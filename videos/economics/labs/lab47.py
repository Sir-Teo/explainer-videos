"""Lab 47: political economy on the Island and in the Data Room: Olson's free riding, the sugar contest, the
build-or-lobby game, Tullock's dissipation, probabilistic voting with and without a lobby, the Senate's close
elections by local linear regression discontinuity, the agency threshold and lame-duck mayors, the franchise, the
rainfall instrument and the political business cycle."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import politics
from explainer.economics.island import truths

TITLE = "Political economy"
GOAL = ("Find how a group's lobbying falls with its size; solve a lobbying contest and measure its waste; see what "
        "swing voters and an organized group receive; estimate the value of barely winning a Senate seat and check "
        "it across bandwidths; find the rents voters must tolerate; map when an elite extends the vote; and recover "
        "the effect of growth on conflict with an instrument.")
TASKS = [
    "Tullock: give one of five players double weight (their spending counts twice). Solve the first-order "
    "conditions numerically: how much does each spend, and what share of the prize is dissipated?",
    "The Senate: estimate the jump with a uniform kernel at bandwidths 5, 10, 20 and 40. Which estimates move most, "
    "and why do narrow bandwidths have larger standard errors?",
    "Conflict: raise the measurement error in growth from 4 to 8 points. How far does least squares move from the "
    "planted -2, and does two-stage least squares follow it?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(47)

    O = T["olson"]
    ns = np.array([1, 4, 25, 100])
    e = politics.olson_effort(O["B"], ns, O["K"])
    lab.row("Olson: a group's total effort for 1, 4, 25 and 100 members", ", ".join(f"{x:.2f}" for x in e))
    assert e[0] > e[1] > e[2] >= e[3]

    g = politics.group_contest(**T["sugar"])
    lab.row("sugar: stake per farm; per consumer; probability the program survives",
            f"${g['v_small']:,.0f}; ${g['v_large']:.2f}; {g['p_pass']:.5f}")

    K = politics.tokens_game(**T["tokens"])
    lab.row("build or lobby: everyone builds; equilibrium lobbying each; equilibrium payoff",
            f"{K['best_payoff']:.0f}; {K['nash_lobby']:.0f}; {K['nash_payoff']:.0f}")

    tl = [politics.tullock(1.0, n)["dissipated"] for n in (2, 5, 10, 100)]
    lab.row("Tullock: share of the prize dissipated with 2, 5, 10, 100 players",
            ", ".join(f"{100 * x:.0f}%" for x in tl))

    V = T["voting"]
    plain = politics.probabilistic_voting(V["alpha"], V["phi"], V["income"])
    lobby = politics.probabilistic_voting(V["alpha"], V["phi"], V["income"], V["organized"], V["h"])
    lab.row("voting: transfers to poor, middle, rich (shares of average income)",
            ", ".join(f"{x:+.2f}" for x in plain["transfer"]))
    lab.row("voting with the rich organized: the same transfers", ", ".join(f"{x:+.2f}" for x in lobby["transfer"]))

    d = data.rdsenate()
    x, y = np.array(d["margin"], float), np.array(d["vote"], float)
    for h in (10.0, 17.754, 50.0):
        r = politics.rd_local_linear(x, y, h)
        lab.row(f"Senate: the jump at bandwidth {h:g} (s.e.)", f"{r['jump']:.2f} ({r['se']:.2f})")

    for W in (0.0, 0.2, 0.5):
        a = politics.agency(W, 1.0, 0.6)
        lab.row(f"agency: tolerated rents with W = {W}, delta = 0.6", f"{a['r_star']:.2f}")
    M = politics.mayors(**{**T["mayors"], "seed": T["mayors"]["seed"] + seed})
    lab.row("mayors: first-term and lame-duck shares taken; how much less", f"{100 * M['first_term']:.1f}%, "
            f"{100 * M['lame_duck']:.1f}%; {100 * M['fewer']:.0f}%")

    F = T["franchise"]
    for q in (0.1, 0.5, 0.9):
        f = politics.franchise(q, 0.6, **F)
        lab.row(f"the franchise with crises a share {q} of years", f"{f['outcome']} (promises worth "
                f"{f['V_promise']:.1f}, revolution {f['V_revolution']:.1f})")

    C = politics.rain_conflict(**{**T["conflict"], "seed": T["conflict"]["seed"] + seed})
    lab.row("conflict: OLS; 2SLS (s.e.); first-stage F; planted -2",
            f"{C['ols']:.2f}; {C['iv']:.2f} ({C['iv_se']:.2f}); {C['F']:.0f}")

    cyc = politics.election_cycle(**T["cycle"])
    lab.row("the cycle: unemployment in the last year of each term (elected; delegated)",
            ", ".join(f"{cyc['u'][t]:.1f}" for t in range(3, 16, 4)) + "; " +
            ", ".join(f"{cyc['u_delegated'][t]:.1f}" for t in range(3, 16, 4)))

    lab.note = ("Free riding makes small groups with large stakes win; a contest for a privilege wastes most of it; "
                "parties court swing and organized groups; barely winning a Senate seat is worth about seven points "
                "next time, at any sensible bandwidth; a job worth keeping lowers the rents voters must tolerate; "
                "an elite rarely threatened extends the vote; and measurement error biases least squares toward zero, "
                "which the rainfall instrument undoes.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    b = politics.rd_bins(x, y, -50, 50, 2.5)
    ax[0].scatter(b["mids"], b["means"], s=14, color=labs.BLUE)
    r = politics.rd_local_linear(x, y, 17.754)
    ax[0].axvline(0, color="black", lw=1)
    ax[0].set(title=f"the Senate: a jump of {r['jump']:.1f} points", xlabel="margin at this election",
              ylabel="vote share at the next")
    ns = np.arange(1, 121)
    ax[1].plot(ns, politics.olson_effort(O["B"], ns, O["K"]), color=labs.ORANGE)
    ax[1].set(title="Olson: a group's total effort", xlabel="members", ylabel="effort")
    lab.fig = fig
    return lab
