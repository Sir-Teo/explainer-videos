"""Lab 28: a thermostat and a defended body weight, a hijacked learner, the ego-depletion replication's meta-analysis
recomputed from its open data, waiting under uncertainty, and a discount curve by titration."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import drive as D

TITLE = "Motivation"
GOAL = ("Derive the thermostat's steady error and remove it; put a diet into an energy-balance loop with and without "
        "a defended set point; watch a learner abandon food for a current; recompute the ego-depletion "
        "replication's pooled effect from its 23 laboratories; and measure discount curves by titration.")
TASKS = [
    "Give the defended weight model a set point that drifts toward the current weight at 1% a day. Does the "
    "regain after the diet shrink? This is the settling point and set point mixed.",
    "Recompute the replication's pooled effect separately for English-speaking and other laboratories. Is the "
    "difference larger than the intervals allow?",
    "Add logistic noise (noise=5) to the titration chooser and run 200 seeds. How far is the fitted k from the "
    "truth, and is the area under the curve more stable?",
]


def run(seed=0):
    out = labs.Lab()

    # 1. the thermostat
    dist = lambda t: -1.0 if t >= 20 else 0.0  # noqa: E731
    p = D.thermostat(T=120.0, k=0.2, disturbance=dist)
    pi = D.thermostat(T=200.0, k=0.2, ki=0.05, disturbance=dist)
    out.row("thermostat at rest after the window opens: proportional, with an integral term (set 20 C)",
            f"{p['x'][-1]:.2f}, {pi['x'][-1]:.2f}")
    assert abs(p["x"][-1] - 15.0) < 0.01 and abs(pi["x"][-1] - 20.0) < 0.05

    # 2. weight
    settle = D.body_weight()
    defend = D.body_weight(hunger=60.0, thrift=25.0)
    out.row("kg lost after 300 days of a 500-kcal cut: static rule, settling point, defended",
            f"{80 - D.static_rule()[399]:.1f}, {80 - settle['W'][399]:.1f}, {80 - defend['W'][399]:.1f}")
    assert 80 - defend["W"][399] < 80 - settle["W"][399] < 80 - D.static_rule()[399]

    # 3. the learner and the current
    for v in (0.5, 1.0, 1.5):
        r = D.self_stimulation(stim=1, stim_value=v, seed=seed)
        out.row(f"current worth {v}: share of presses on it, energy store (last 1,000 presses)",
                f"{r['choice'][-1000:].mean():.2f}, {r['energy'][-1000:].mean():.2f}")

    # 4. the registered replication
    d = opendata.ego_depletion_rrr()
    g, v = [], []
    for i in range(len(d["lab"])):
        if d["original"][i]:
            continue
        gi, vi = D.hedges_g(d["m_dep"][i], d["sd_dep"][i], d["n_dep"][i], d["m_ctl"][i], d["sd_ctl"][i],
                            d["n_ctl"][i])
        g.append(gi)
        v.append(vi)
    re = D.random_effects(g, v)
    out.row("RRR: laboratories; pooled d [95% CI]; I^2",
            f"{re['k']}; {re['estimate']:.2f} [{re['lo']:.2f}, {re['hi']:.2f}]; {100 * re['I2']:.0f}%")
    assert re["k"] == 23 and abs(re["estimate"] - 0.04) < 0.01

    # 5. waiting
    for kind in ("normal", "pareto"):
        w = D.remaining_wait([0.0, 5.0, 10.0], kind)
        out.row(f"{kind} return: expected further wait at 0, 5, 10 minutes; best give-up time",
                f"{w[0]:.1f}, {w[1]:.1f}, {w[2]:.1f}; {D.give_up_time(kind)['best']:.1f}")

    # 6. discounting
    for k in (0.002, 0.02, 0.1):
        r = D.discount_titration(k)
        out.row(f"titration, true k = {k}: fitted k, area under the curve", f"{r['k_fit']:.4f}, {r['auc']:.2f}")
        assert abs(r["k_fit"] / k - 1) < 0.1

    out.note = ("Proportional control leaves an error an integral term removes; a defended set point stiffens the loop "
                "so a diet loses less; a learner given a reward that bypasses the body abandons food; 23 "
                "laboratories pool to almost nothing; heavy-tailed waits make quitting rational; and six questions "
                "per delay recover a discount rate.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(settle["day"], settle["W"], color=labs.BLUE, label="settling point")
    ax[0].plot(defend["day"], defend["W"], color=labs.GOLD, label="defended set point")
    ax[0].set(title="A 500-kcal diet, days 100 to 400", xlabel="day", ylabel="weight (kg)")
    ax[0].legend()
    order = np.argsort(g)
    se = np.sqrt(np.array(v))[order]
    ax[1].errorbar(np.array(g)[order], np.arange(len(g)), xerr=1.96 * se, fmt="s", color=labs.BLUE)
    ax[1].axvline(re["estimate"], color=labs.GOLD)
    ax[1].axvline(0, ls="--", color="#888888")
    ax[1].set(title="The ego-depletion replication, by laboratory", xlabel="Hedges's g", ylabel="laboratory")
    out.fig = fig
    return out
