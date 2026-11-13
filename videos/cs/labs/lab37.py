"""Lab 37: run Chiu and Jain's four rules from a random start, and solve Kelly's problem with link prices."""

from videos.coursekit import labs

import numpy as np

from explainer.cs.net import cc

TITLE = "Only AIMD is fair, and TCP is an optimizer"
GOAL = ("Start two users at unequal rates on one link and run AIMD, AIAD, MIMD and MIAD from Chiu and Jain's model: "
        "check that an additive step keeps the difference, a multiplicative step keeps the ratio, and only AIMD "
        "reaches Jain's index 1. Then solve Kelly's utility maximization on two links by dual ascent on prices and "
        "compare it with the closed form (1/3, 2/3, 2/3).")
TASKS = [
    "Change AIMD's decrease factor b from 0.5 to 0.9. How many decreases does it take to halve the unfairness now?",
    "Give the long flow a third link (routes 'long': ['L1', 'L2', 'L3']). What rates and prices does dual ascent find?",
    "Raise the dual step from 0.05 to 2.5. What happens to the prices, and what does that say about gain in a control loop?",
]
RULES = ("AIMD", "AIAD", "MIMD", "MIAD")


def run(seed=0):
    rng = np.random.default_rng(seed)
    x0 = (float(rng.uniform(0.05, 0.25)), float(rng.uniform(0.5, 0.8)))
    lab = labs.Lab()
    lab.row("start (user 1, user 2)", f"({x0[0]:.3f}, {x0[1]:.3f})   Jain's index {cc.jain(x0):.3f}")
    out = {rule: cc.chiu_jain(rule, x0=x0, steps=200, a=0.03, b=0.5, m=1.15) for rule in RULES}
    for rule in RULES:
        r = out[rule]
        x1, x2 = r["trajectory"][-1]
        lab.row(f"{rule}: after 200 rounds", f"({x1:.3f}, {x2:.3f})   fairness {r['fairness']:.3f}   load {r['efficiency']:.2f}")
    diff0, ratio0 = x0[1] - x0[0], x0[1] / x0[0]
    t = np.array(out["AIMD"]["trajectory"])
    halvings = int(np.sum(t[1:].sum(axis=1) < t[:-1].sum(axis=1)))
    assert abs((t[-1, 1] - t[-1, 0]) - diff0 * 0.5 ** halvings) < 1e-9, "each halving halves the difference, exactly"
    assert out["AIMD"]["fairness"] > 0.999 and 0.7 < out["AIMD"]["efficiency"] < 0.82, "AIMD: fair, about 3/4 full"
    t = np.array(out["AIAD"]["trajectory"])
    assert np.allclose(t[:, 1] - t[:, 0], diff0), "AIAD never changes the difference"
    t = np.array(out["MIMD"]["trajectory"])
    assert np.allclose(t[:, 1] / t[:, 0], ratio0), "MIMD never changes the ratio"
    assert out["AIAD"]["fairness"] < 0.97 and out["MIMD"]["fairness"] < 0.9
    assert out["MIAD"]["fairness"] < 0.55 and out["MIAD"]["trajectory"][-1][0] < 1e-9, "MIAD starves user 1"
    lab.row("AIMD: decreases, and the difference left", f"{halvings} halvings; {diff0:.3f} x 0.5^{halvings} = {diff0 * 0.5 ** halvings:.1e}")

    # Kelly: maximize the sum of log rates; a long flow crosses both links, a short flow uses each one
    routes, caps = {"long": ["L1", "L2"], "a": ["L1"], "b": ["L2"]}, {"L1": 1.0, "L2": 1.0}
    num = cc.num_dual(routes, caps, step=0.05, iters=3000)
    fair = cc.max_min(routes, caps)
    x, p = num["x"], num["p"]
    lab.row("dual ascent: rates (long, a, b)", f"{x['long']:.3f}, {x['a']:.3f}, {x['b']:.3f}   closed form 0.333, 0.667, 0.667")
    lab.row("dual ascent: link prices", f"{p['L1']:.3f}, {p['L2']:.3f}   closed form 1.5, 1.5")
    lab.row("max-min fair rates", f"{fair['long']:.3f}, {fair['a']:.3f}, {fair['b']:.3f}   total {sum(fair.values()):.3f} against {sum(x.values()):.3f}")
    assert abs(x["long"] - 1 / 3) < 0.01 and abs(x["a"] - 2 / 3) < 0.01 and abs(x["b"] - 2 / 3) < 0.01
    assert abs(p["L1"] - 1.5) < 0.03 and abs(p["L2"] - 1.5) < 0.03, "the prices are the Lagrange multipliers"
    assert all(abs(v - 0.5) < 1e-9 for v in fair.values()) and sum(x.values()) > sum(fair.values()) + 0.15
    lab.note = ("Adding moves the pair along a 45-degree line and multiplying along a line through the origin, so only "
                "additive increase with multiplicative decrease closes the gap; and rates that answer link prices "
                "settle at the proportionally fair optimum, which carries more in total than max-min fairness.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot([0, 1], [1, 0], color=labs.MUTED, ls="--", lw=1, label="efficient: x1 + x2 = C")
    ax[0].plot([0, 1], [0, 1], color=labs.GREY, ls=":", lw=1.2, label="fair: x1 = x2")
    for rule, color in zip(RULES, (labs.GREEN, labs.BLUE, labs.GOLD, labs.RED)):
        t = np.array(out[rule]["trajectory"])
        ax[0].plot(t[:, 0], t[:, 1], color=color, lw=1.3, label=rule)
    ax[0].scatter(*x0, color=labs.INK, s=30, zorder=3)
    ax[0].set(title="Chiu and Jain's plane: four rules from one start", xlabel="user 1's rate", ylabel="user 2's rate",
              xlim=(0, 1.2), ylim=(0, 1.2), aspect="equal")
    ax[0].legend(loc="upper right")
    h = num["history"]
    its = [r["iter"] for r in h]
    ax[1].plot(its, [r["x"]["long"] for r in h], color=labs.RED, label="long flow (both links)")
    ax[1].plot(its, [r["x"]["a"] for r in h], color=labs.BLUE, label="short flow on link 1")
    ax[1].plot(its, [r["p"]["L1"] for r in h], color=labs.GOLD, label="price of link 1")
    for y in (1 / 3, 2 / 3, 1.5):
        ax[1].axhline(y, color=labs.MUTED, ls="--", lw=0.9)
    ax[1].set(title="Dual ascent: prices rise until demand fits", xlabel="iteration", ylabel="rate, or price",
              xlim=(0, 1500), ylim=(0, 2.2))
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
