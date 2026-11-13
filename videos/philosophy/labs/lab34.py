"""Lab 34: build Press and Dyson's extortioner for any ratio, and check equilibria and the shadow of the future."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import games

TITLE = "Extortion on a line, equilibria by enumeration, and patience"
GOAL = ("Build the zero-determinant extortioner for ratios 2, 3 and 5 from Press and Dyson's formula, play each "
        "against 400 random memory-one opponents and check that (s_X - P) = chi (s_Y - P) every time; verify the "
        "support-enumeration equilibria by checking every pure deviation; and find the patience grim trigger and "
        "tit for tat need.")
TASKS = [
    "Add 0.05 to the extortioner's p_DD (it now sometimes cooperates after mutual defection). How far do the "
    "opponents' points leave the line?",
    "Play the chi = 3 extortioner against itself and against tit for tat. Who gets what, and why does an "
    "extortioner lose a tournament it never loses a match in?",
    "Change the payoffs to (T, R, P, S) = (4, 3, 1, 0) in games.PD and rerun. Which thresholds for grim and tit "
    "for tat move, and to what?",
]

T, R, P, S = (games.PD[k] for k in "TRPS")


def extortioner(chi, share=0.5):
    """p = (p_CC, p_CD, p_DC, p_DD) with p~ = phi [(S_X - P) - chi (S_Y - P)]; phi is `share` of its largest value."""
    phi = share / ((T - P) * chi + (P - S))
    return [1 - phi * (chi - 1) * (R - P), 1 - phi * ((P - S) + chi * (T - P)), phi * ((T - P) + chi * (P - S)), 0.0]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    opponents = rng.random((400, 4))
    clouds = {}
    for chi in (2, 3, 5):
        p = extortioner(chi)
        pts = np.array([games.payoffs_memory_one(p, q) for q in opponents])
        ok = np.abs(pts[:, 1] - P) > 1e-3
        ratio = (pts[ok, 0] - P) / (pts[ok, 1] - P)
        clouds[chi] = pts
        lab.row(f"chi = {chi}: p = ({', '.join(f'{v:.3f}' for v in p)})",
                f"(s_X - P)/(s_Y - P) from {ratio.min():.5f} to {ratio.max():.5f} over {ok.sum()} opponents")
        assert np.all(np.abs(ratio - chi) < 1e-4), "the extortioner enforces its ratio against every opponent"
        assert np.all(pts[:, 0] >= pts[:, 1] - 1e-6), "and never scores less than its opponent"
    zd = games.zero_determinant(n_opponents=200, seed=2012 + seed)
    assert np.allclose(extortioner(3), [11 / 13, 1 / 2, 7 / 26, 0]) and np.allclose(extortioner(3), zd["extortioner"],
                                                                                   atol=1e-4)
    assert abs(zd["equalized_min"] - 2) < 1e-4 and abs(zd["equalized_max"] - 2) < 1e-4, "the equalizer pins s_Y at 2"
    plain = np.array([games.payoffs_memory_one([0.9, 0.5, 0.5, 0.1], q) for q in opponents])
    spread = np.ptp((plain[:, 0] - P) / (plain[:, 1] - P))
    lab.row("an ordinary strategy (0.9, 0.5, 0.5, 0.1): the same ratio", f"varies by {spread:.2f} across opponents")
    lab.row("the chi = 3 extortioner against itself", f"{zd['against_itself']:.3f} each   (P = {P})")
    assert spread > 0.5 and abs(zd["against_itself"] - P) < 0.01

    counts = {}
    for name, (A, B, _) in games.GAMES.items():
        A, B = np.array(A, float), np.array(B, float)
        eqs = games.nash_equilibria(A, B)
        counts[name] = len(eqs)
        for e in eqs:  # no pure deviation gains: enough, since a mixed deviation is an average of pure ones
            x, y = np.array(e["row"]), np.array(e["col"])
            assert np.max(A @ y) <= x @ A @ y + 1e-3 and np.max(x @ B) <= x @ B @ y + 1e-3, name
    lab.row("Nash equilibria found", ",  ".join(f"{k}: {v}" for k, v in counts.items()))
    assert counts == {"prisoner's dilemma": 1, "matching pennies": 1, "battle of the sexes": 3, "stag hunt": 3,
                      "chicken": 3}
    A, B = rng.normal(size=(3, 3)), rng.normal(size=(3, 3))
    eqs = games.nash_equilibria(A, B)
    for e in eqs:
        x, y = np.array(e["row"]), np.array(e["col"])
        assert np.max(A @ y) <= x @ A @ y + 1e-3 and np.max(x @ B) <= x @ B @ y + 1e-3
    lab.row("a random 3 x 3 game", f"{len(eqs)} equilibria, each checked against every pure deviation")
    assert len(eqs) % 2 == 1, "a nondegenerate game has an odd number of equilibria, so at least one"

    deltas = np.round(np.arange(0.40, 0.801, 0.02), 2)
    sh = games.shadow(deltas)
    lab.row("least patience for cooperation against grim, tit for tat",
            f"{sh['grim']['threshold_grid']:.2f}, {sh['tft']['threshold_grid']:.2f} on a grid of 0.02   "
            f"(theory {sh['grim']['threshold']:.3f}, {sh['tft']['threshold']:.3f})")
    assert sh["grim"]["threshold_grid"] == 0.5 and 0.66 <= sh["tft"]["threshold_grid"] <= 0.68
    lab.note = ("A memory-one player can fix a linear relation between the two long-run scores whatever the other "
                "does: the points of 400 opponents fall on a line through (P, P) with slope chi. An opponent "
                "raises its own score only by cooperating more, which pays the extortioner chi times as much.")

    fig, ax = labs.figure(2, size=(11.5, 4.4))
    for chi, color in ((2, labs.BLUE), (3, labs.GOLD), (5, labs.RED)):
        ax[0].scatter(clouds[chi][:, 1], clouds[chi][:, 0], s=6, color=color, label=f"extortioner, chi = {chi}")
    ax[0].scatter(plain[:, 1], plain[:, 0], s=6, color=labs.MUTED, alpha=0.6, label="(0.9, 0.5, 0.5, 0.1)")
    ax[0].plot([0, 5], [0, 5], color=labs.GRID, lw=1)
    ax[0].set(title="400 random opponents against four strategies", xlabel="opponent's score s_Y",
              ylabel="the strategy's score s_X")
    ax[0].legend(loc="upper left")
    for key, label, color in (("cooperate", "cooperate for ever", labs.GREEN),
                              ("always_defect", "defect for ever", labs.RED),
                              ("alternate", "alternate D, C", labs.GOLD)):
        ax[1].plot(deltas, sh["curves"][key], color=color, label=label)
    ax[1].plot(deltas, sh["tft"]["best"], "o", ms=3, color=labs.INK, label="best of the 32 strategies")
    ax[1].axvline(2 / 3, color=labs.MUTED, ls=":")
    ax[1].set(title="Replies to tit for tat, by patience", xlabel="discount factor delta",
              ylabel="normalized discounted payoff")
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
