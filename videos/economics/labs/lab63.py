"""Lab 63: the economy as a network: Domar weights and Leontief's paths, Hulten's theorem and its second-order terms,
granular and network volatility, a supply-chain disaster, the O-ring, clearing and contagion, diffusion, the key
player, network formation, fragility, and the Dials' Island estimates."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import network as N

TITLE = "The economy as a network"
GOAL = ("Turn the Island's input-output table into a network, test Hulten's theorem and break it, and follow shocks "
        "along supply chains, between banks and through villages.")
TASKS = [
    "Make every input easy to substitute (N.which_failure(theta=1.5)). Which sector's failure now costs more or less "
    "than its sales predict?",
    "Give every firm more possible suppliers (N.quake(replace_specific=0.6)). How much of the Island's loss do the "
    "links still add?",
    "Cut the banks' cushion to zero (N.contagion(buffer=0.0)). Where does the complete network now fail?",
]


def run(seed=0):
    lab = labs.Lab()
    L = N.leontief()
    lab.row("Domar weights (sales over GDP), and their sum",
            ", ".join(f"{s} {d:.2f}" for s, d in zip(N.SECTORS, L["domar"])) + f"; sum {L['sum_domar']:.2f}")
    H = N.which_failure(shock=-0.1, theta=1.0)
    gap = max(abs(r["loss"] - r["hulten"]) for r in H["rows"])
    assert gap < 1e-9                                             # Hulten's theorem, exactly, for Cobb-Douglas
    lab.row("Hulten checked: largest gap between computed and lambda x shock (Cobb-Douglas)", f"{gap:.1e}")
    P = N.which_failure(shock=-0.5, theta=0.15)
    lab.row("a loss of 0.5 log points, elasticity 0.15: GDP's fall, computed (Hulten), %",
            ", ".join(f"{r['sector']} {100 * (1 - np.exp(r['loss'])):.1f} ({100 * (1 - np.exp(r['hulten'])):.1f})"
                      for r in P["rows"]))
    G = N.granular(seed=63 + seed)
    lab.row("GDP's swing from 12% firm shocks, 10,000 firms: equal, Zipf",
            f"{100 * G['rows'][-1]['equal']:.2f}%, {100 * G['rows'][-1]['zipf']:.2f}%")
    Q = N.quake(seed=63 + seed)
    lab.row("the quake: loss downstream at 1, 2, 3 steps; upstream; total against the hit firms alone",
            ", ".join(f"{100 * r['loss']:.1f}" for r in Q["rows"]["downstream"]) + "; " +
            ", ".join(f"{100 * r['loss']:.1f}" for r in Q["rows"]["upstream"]) +
            f"; {100 * Q['total_loss']:.1f}% against {100 * Q['direct_only']:.1f}%")
    O = N.oring(seed=63 + seed)
    lab.row("the O-ring: sorting's gain over random teams", f"{100 * O['gain']:.1f}%")
    C = N.contagion()
    thr = next(s for s, d in zip(C["shocks"], C["complete"]["defaults"]) if d == 10)
    lab.row("contagion: defaults at a loss of 5 (ring, complete); the complete network's breaking point",
            f"{C['ring']['defaults'][5]}, {C['complete']['defaults'][5]}; {thr:.0f}")
    D = N.diffusion(reps=150, seed=63 + seed)
    lab.row("diffusion after 8 rounds: most central, random, least central seeds",
            f"{100 * D['most central'][-1]:.0f}%, {100 * D['at random'][-1]:.0f}%, {100 * D['least central'][-1]:.0f}%")
    K = N.key_player()
    lab.row("the key player against the player with most links", f"player {K['key']} (removal costs "
            f"{100 * K['drop'][K['key']] / K['total']:.0f}%) against {K['most_links']} "
            f"({100 * K['drop'][K['most_links']] / K['total']:.0f}%)")
    F = N.formation(costs=[0.1, 0.4, 0.8, 1.1])
    lab.row("formation (links in the efficient network; star stable?) at c = 0.1, 0.4, 0.8, 1.1",
            ", ".join(f"{r['efficient_links']} ({'yes' if r['star_stable'] else 'no'})" for r in F["rows"]))
    Fr = N.fragility()
    lab.row("fragility: the cliff with 2, 3, 5 suppliers per input",
            ", ".join(f"{Fr[f'n_{n}']['cliff']:.2f}" for n in (2, 3, 5)))
    R = N.granular_residual(reps=200, seed=63 + seed)
    S = N.substitution_estimate(seed=63 + seed)
    lab.row("Dials: granular residual's median R-squared (planted share); elasticity estimate (planted)",
            f"{R['median']:.2f} ({R['truth']:.2f}); {S['estimate']:.3f} ({S['theta']:.2f})")
    f = data.fred("JPNPROINDMISMEI")
    v = np.array([float(x) for x in f["value"]])
    k = f["date"].index("2011-03-01")
    lab.row("Japan's industrial production, March 2011 against February", f"{100 * (v[k] / v[k - 1] - 1):+.1f}%")

    lab.note = ("Hulten's theorem says sales are enough for small shocks; everything after it in this lab is a reason "
                "they are not: unequal firms, lopsided networks, large shocks to essential inputs, specific links, "
                "concentrated debts.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    Rs = N.gdp_response("energy", thetas=(0.15, 1.0, 1.5))
    for key, col in (("theta_0.15", labs.ORANGE), ("theta_1", "k"), ("theta_1.5", "tab:blue")):
        ax[0].plot(Rs["shocks"], Rs[key], color=col, label=key.replace("theta_", "elasticity "))
    ax[0].plot(Rs["shocks"], Rs["hulten"], "k--", lw=1, label="Hulten")
    ax[0].set(title="GDP's response to energy's productivity", xlabel="log change in energy's productivity",
              ylabel="log change in GDP")
    ax[0].legend(fontsize=8)
    for n_ in (2, 3, 5):
        ax[1].plot(Fr["r"], Fr[f"n_{n_}"]["rho"], label=f"{n_} suppliers")
    ax[1].set(title="fragile supply networks", xlabel="strength of a relationship", ylabel="share producing")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
