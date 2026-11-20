"""Lab 26: banks and runs: Diamond and Dybvig's contract and its run threshold, sequential service, Bagehot's lender
against a fire sale, deposit insurance as a put, the repo squeeze, the global game's threshold, and delegated
monitoring."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import bank as bk
from explainer.economics.island import truths

TITLE = "Banks and runs: why a sound bank can fail, and what stops it"
GOAL = ("Solve the Diamond-Dybvig deposit contract and find the share of withdrawals at which waiting stops paying; "
        "run a bank with sequential service; compare a fire sale with Bagehot's lender; price deposit insurance as a "
        "put; compute the repo squeeze; check the global game's threshold by simulation; and see why a diversified bank "
        "can promise fixed payments.")
TASKS = [
    "Diamond-Dybvig: raise risk aversion to 4. How do c1, c2 and the run threshold change, and why is a more "
    "insuring contract more fragile?",
    "Bagehot: at what fire-sale price does the Island's bank survive without a lender?",
    "Global game: with R = 2, what payment to withdrawers makes the bank fail below a strength of 0.75? Check it by "
    "simulation.",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(26)

    D = T["dd"]
    d = bk.dd_contract(R=D["R"], gamma=D["gamma"], t=D["t"])
    assert abs(D["t"] * d["c1"] + (1 - D["t"]) * d["c2"] / D["R"] - 1) < 1e-12 and d["eu"] > d["eu_autarky"]
    lab.row("Diamond-Dybvig: c1, c2 (alone: 1, 1.5)", f"{d['c1']:.3f}, {d['c2']:.3f}")
    stay = bk.dd_stayers([0.25, 0.5, d["threshold"], 0.7], d["c1"], D["R"])
    assert stay[1] > d["c1"] > stay[3]
    lab.row("stayers' payment if 25%, 50%, the threshold, 70% withdraw",
            ", ".join(f"{x:.3f}" for x in stay) + f"  (threshold {100 * d['threshold']:.1f}%)")

    r = bk.sequential_service(n=D["n"], c1=d["c1"], seed=D["seed"] + seed)
    assert abs(r["served"] / D["n"] - 1 / d["c1"]) < 0.002
    lab.row("a run with sequential service: share paid in full", f"{r['served']} of {D['n']}")

    L = bk.lender_of_last_resort(**T["llr"])
    assert not L["survives_fire"] and L["survives_llr"]
    lab.row("Bagehot: equity after a fire sale; with a lender", f"{L['equity_fire']:.2f}; {L['equity_llr']:.2f}")

    M = T["merton"]
    puts = [bk.merton_put(M["V"], M["D"], s) for s in M["sigmas"]]
    assert all(abs(p["equity"] - p["put"] - (M["V"] - M["D"])) < 1e-9 for p in puts)
    lab.row("Merton's put at 5%, 10%, ..., 25% volatility", ", ".join(f"{p['put']:.2f}" for p in puts))

    S = T["sheet"]
    b = bk.bond_loss(S["coupon"], S["years"], S["y0"], S["y1"])
    lab.row("a ten-year bond when yields rise 1.5% to 4.5%: change; duration",
            f"{100 * b['change']:.1f}%; {b['duration']:.2f} years")

    rp = T["repo"]
    q = bk.repo_leverage(rp["assets"], rp["equity"], rp["haircut_from"], rp["haircut_to"])
    assert abs(q["must_sell"] - 80) < 1e-9
    lab.row("repo: haircut 4% to 20%: must sell", f"{q['must_sell']:.0f} of {rp['assets']:.0f}")

    G = T["gg"]
    g = bk.global_game(c=G["c"], R=G["R"], sigma=G["sigma"], n=G["n"], seed=G["seed"] + seed)
    th, fail = np.array(g["theta"]), np.array(g["fail"])
    edge = float(th[~fail].min())
    assert abs(edge - g["theta_star"]) < 0.05
    lab.row("global game: theta* = c/R; the simulated edge of failure", f"{g['theta_star']:.2f}; {edge:.2f}")

    Mo = T["monitor"]
    pf = [bk.diversified_failure(n, Mo["p"], Mo["R"], Mo["D"]) for n in Mo["ns"]]
    assert pf[0] > pf[1] > pf[2] > pf[3]
    lab.row("delegated monitoring: failure with 1, 10, 100, 1,000 loans", ", ".join(f"{x:.2e}" for x in pf))

    sus = data.fred("X14AICBS")
    yrs = [int(x[:4]) for x in sus["date"]]
    v33, v34 = sus["value"][yrs.index(1933)], sus["value"][yrs.index(1934)]
    assert v33 > 50 * v34
    lab.row("US bank suspensions, 1933 and 1934", f"{v33:.0f} and {v34:.0f}")

    lab.note = ("A deposit contract that insures people against needing their money early pays more than the bank can "
                "pay everyone at once, so it has a second equilibrium: once enough people are expected to withdraw, "
                "everyone should. Insurance and a lender of last resort remove it; a fire sale turns illiquidity into "
                "insolvency. With a little private noise the run becomes predictable: the bank fails exactly when its "
                "strength is below c/R.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    f = np.linspace(0, 0.85, 171)
    ax[0].plot(100 * f, bk.dd_stayers(f, d["c1"], D["R"]), color=labs.BLUE, label="stay")
    ax[0].axhline(d["c1"], color=labs.ORANGE, label="withdraw")
    ax[0].axvline(100 * d["threshold"], color="grey", lw=0.8)
    ax[0].set(title="Diamond-Dybvig: stay or withdraw?", xlabel="share withdrawing, %", ylabel="payment", ylim=(0, 2))
    ax[0].legend()
    ax[1].plot(th, g["share"], color=labs.ORANGE, label="share withdrawing")
    ax[1].plot([0, 1], [0, 1], color="grey", lw=0.8, ls="--")
    ax[1].axvline(g["theta_star"], color=labs.BLUE, lw=1.2, label="theta* = c/R")
    ax[1].set(title="The global game", xlabel="the bank's strength", ylabel="share withdrawing")
    ax[1].legend()
    lab.fig = fig
    return lab
