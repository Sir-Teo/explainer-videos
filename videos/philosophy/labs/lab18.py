"""Lab 18: sample a 2D Ising model below, at and above the critical temperature and coarse-grain it by block spins."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import science as Sc

TITLE = "Block spins: the flow to order, to disorder, and the fixed point"
GOAL = ("Sample an 81 by 81 Ising lattice with the Reasoner's Swendsen-Wang sampler at T = 2.0, at Onsager's "
        "critical temperature and at T = 2.6, then replace each 3 by 3 block by its majority, twice. The "
        "neighbour correlation must rise below the critical temperature, fall above it, and barely move at it; "
        "the magnetization at T = 2.0 is checked against Onsager's exact value.")
TASKS = [
    "Move the two outer temperatures towards the critical one (2.2 and 2.35). How many blocking steps does it now "
    "take to tell them from the fixed point, and what would a larger lattice change?",
    "Replace the majority rule by decimation (keep the centre spin of each block). Does the flow still separate "
    "the three temperatures?",
    "Use Sc.no_miracles to find the base rate at which a successful theory is as likely false as true, then make "
    "false theories succeed 20% of the time and find it again.",
]


def flow(T, seed, L=81, burn=100, samples=10, gap=15):
    """Mean neighbour correlation at each blocking level (81, 27, 9), and mean |m|, over several samples."""
    s = Sc.ising_sw(L, T, burn, seed, np.ones((L, L), int) if T < Sc.TC else None)
    corr, mags = [], []
    for k in range(samples):
        s = Sc.ising_sw(L, T, gap, seed + 1000 + k, s)
        levels = [s, Sc.block_spin(s)]
        levels.append(Sc.block_spin(levels[1]))
        corr.append([Sc.nn_corr(x) for x in levels])
        mags.append(abs(s.mean()))
    return np.mean(corr, axis=0), float(np.mean(mags)), levels


def run(seed=0):
    lab = labs.Lab()
    temps = [("below: T = 2.0", 2.0), ("critical: T = 2.269", Sc.TC), ("above: T = 2.6", 2.6)]
    out = {}
    for i, (name, T) in enumerate(temps):
        out[name] = flow(T, 100 * seed + i)
        c = out[name][0]
        lab.row(f"{name}: neighbour correlation at 81, 27, 9", "   ".join(f"{x:.3f}" for x in c))
    lo, mid, hi = (out[name][0] for name, _ in temps)
    assert lo[0] < lo[1] < lo[2] and lo[2] > 0.97, "below T_c the blocked lattice flows to order"
    assert hi[0] > hi[1] > hi[2] and hi[2] < 0.4, "above T_c it flows to disorder"
    assert abs(mid[1] - mid[0]) < 0.7 * min(lo[1] - lo[0], hi[0] - hi[1]), "at T_c one blocking barely moves it"
    assert hi[2] < mid[2] < lo[2]
    m, exact = out[temps[0][0]][1], Sc.onsager_m(2.0)
    assert abs(m - exact) < 0.03, "Onsager's magnetization"
    lab.row("|m| at T = 2.0: sampled, Onsager's exact value", f"{m:.3f}   {exact:.3f}")
    nm = [Sc.no_miracles(b) for b in (0.5, 0.05, 0.01)]
    assert abs(nm[0] - 0.95) < 1e-9 and abs(nm[1] - 0.5) < 1e-9 and nm[2] < 0.2
    lab.row("P(true | successful) at base rates 0.5, 0.05, 0.01", "   ".join(f"{x:.2f}" for x in nm))
    lab.note = ("Coarse-graining throws detail away, and what survives depends only on which side of the critical "
                "temperature the lattice is on: that insensitivity to microscopic detail is what universality "
                "means, and why Batterman calls the explanation emergent.")

    fig = labs.figure(1, size=(11, 4.4))[0]
    fig.clear()
    grid = fig.add_gridspec(2, 5, width_ratios=[1, 1, 1, 0.15, 2.2])
    for i, (name, T) in enumerate(temps):
        for j, lv in enumerate((out[name][2][0], out[name][2][2])):
            a = fig.add_subplot(grid[j, i])
            a.imshow(lv, cmap="cividis", vmin=-1, vmax=1, interpolation="nearest")
            a.set_xticks([])
            a.set_yticks([])
            a.grid(False)
            a.set_title(name if j == 0 else "blocked twice (9 x 9)", fontsize=9)
    a = fig.add_subplot(grid[:, 4])
    for (name, T), color in zip(temps, (labs.BLUE, labs.GOLD, labs.RED)):
        a.plot([0, 1, 2], out[name][0], marker="o", color=color, label=name)
    a.set_xticks([0, 1, 2], ["81 x 81", "27 x 27", "9 x 9"])
    a.set(title="Neighbour correlation under block-spin steps", xlabel="lattice after blocking", ylim=(0, 1.05))
    a.legend(loc="lower left")
    lab.fig = fig
    return lab
