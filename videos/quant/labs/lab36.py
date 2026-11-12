"""Lab 36: which queue empties first, and orders that arrive in clusters."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import sim

TITLE = "The next tick from the queues, and clustered order flow"
GOAL = ("Two queues sit at the best bid and ask; the price ticks up when the ask empties first. Simulate that "
        "race from every starting pair, compare with the closed form and with the naive imbalance, then simulate "
        "a self-exciting order flow and recover its branching ratio by maximum likelihood.")
TASKS = [
    "Let the bid queue shrink faster than the ask (a seller is working an order). How does the picture tilt?",
    "Raise the branching ratio to 0.95. What happens to the event rate and to the fit's uncertainty?",
    "Turn the up-probability into a microprice: mid + (2u - 1) x half a tick. When is it far from the weighted mid?",
]


def depletion_prob(bid, ask, n_paths, rng, max_steps=40000):
    """P(the ask queue empties before the bid): each step one queue, chosen at random, moves by +-1.

    The race has no finite expected length (a driftless walk in a quadrant), so it is cut at ``max_steps``; the
    few undecided paths are left out."""
    b = np.full(n_paths, bid)
    a = np.full(n_paths, ask)
    ups = downs = 0
    for _ in range(max_steps):
        which = rng.random(b.size) < 0.5
        step = np.where(rng.random(b.size) < 0.5, 1, -1)
        b = b + np.where(which, step, 0)
        a = a + np.where(which, 0, step)
        ups += int(np.sum(a == 0))
        downs += int(np.sum(b == 0))
        live = (a > 0) & (b > 0)
        b, a = b[live], a[live]
        if b.size == 0:
            break
    return ups / (ups + downs)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    pairs = [(9, 3), (6, 6), (3, 9), (12, 2), (5, 4)]
    worst = 0.0
    sim_u, th_u, imb = [], [], []
    for bid, ask in pairs:
        u = depletion_prob(bid, ask, 6000, rng)
        theory = 1 - 2 / np.pi * np.arctan(ask / bid)  # harmonic in the quadrant: Brownian queues
        sim_u.append(u), th_u.append(theory), imb.append(bid / (bid + ask))
        worst = max(worst, abs(u - theory))
        lab.row(f"bid {bid:>2}, ask {ask:>2}", f"P(up) simulated {u:.3f}   formula {theory:.3f}   imbalance {bid / (bid + ask):.3f}")
    events = sim.hawkes_thinning(1.0, 1.4, 2.0, 2000.0, seed=seed)
    fit = sim.hawkes_fit(events, 2000.0)
    lab.row("Hawkes flow: true branching 0.70", f"fitted {fit['branching']:.3f}; rate {len(events) / 2000:.2f}/s "
                                                f"(theory mu / (1 - n) = {1 / 0.3:.2f})")
    lab.note = ("The imbalance is the right direction and the wrong number. And seven orders in ten are "
                "reactions to earlier orders: the flow's clock is not Poisson.")
    assert worst < 0.03 and abs(fit["branching"] - 0.7) < 0.05 and abs(len(events) / 2000 - 1 / 0.3) < 0.4

    fig, ax = labs.figure(2, size=(11, 4.2))
    I = np.linspace(0.02, 0.98, 200)
    ax[0].plot(I, 1 - 2 / np.pi * np.arctan((1 - I) / I), color=labs.P, label="1 - (2/pi) atan(ask/bid)")
    ax[0].plot(I, I, color=labs.MUTED, ls="--", label="imbalance itself")
    ax[0].plot(imb, sim_u, "o", color=labs.SPOT, label="simulated queues")
    ax[0].set(title="Probability the next tick is up", xlabel="imbalance: bid / (bid + ask)")
    ax[0].legend(fontsize=8)
    window = events[events < 60]
    grid = np.linspace(0, 60, 1500)
    ax[1].plot(grid, sim.hawkes_intensity(window, 1.0, 1.4, 2.0, grid), color=labs.OPTION, lw=0.9)
    ax[1].plot(window, np.zeros_like(window), "|", color=labs.SPOT, ms=10)
    ax[1].axhline(1.0, color=labs.MUTED, ls=":", lw=1)
    ax[1].set(title="A minute of self-exciting order flow: intensity and events", xlabel="seconds", ylabel="events per second")
    lab.fig = fig
    return lab
