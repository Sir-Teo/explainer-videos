"""Lab 57: set four learning bounds against measurements: a PAC curve, a growth function, the perceptron, and regret."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import math

import numpy as np

from explainer.cs.learn import theory

TITLE = "Bounds against measurements: PAC, VC, margins, regret"
GOAL = ("Learn a hidden rectangle 200 times at each sample size and compare the error with (4/m) ln(4/delta); count "
        "the labellings half-planes realize against Sauer-Shelah; count the perceptron's mistakes against "
        "(R/gamma)^2; and run Hedge and follow the leader on random losses and against an alternating adversary.")
TASKS = [
    "Change delta from 0.05 to 0.01 in theory.rectangle_curves. How much does the bound move, how much does the measured quantile move, and why so little?",
    "In adversary() give Hedge the learning rate 10 * eta and then eta / 10. Which term of ln N / eta + eta T / 8 grows in each case, and does the measured regret follow it?",
    "Run theory.perceptron_margin with gamma = 0.05 and 0.2. Do the mistakes scale like 1/gamma^2, and does the dimension matter?",
]

T_ROUNDS, N_EXPERTS = 2000, 20


def adversary(T, eta):
    """Two experts whose losses alternate after a first half-loss: the leader is always the one about to lose."""
    L = np.zeros((T, 2))
    L[0] = (0.5, 0.0)
    L[1::2, 1] = 1.0
    L[2::2, 0] = 1.0
    w, cum, hedge, ftl, cum_h, cum_f = np.ones(2), np.zeros(2), [], [], 0.0, 0.0
    for t in range(T):
        cum_h += (w / w.sum()) @ L[t]
        cum_f += L[t, int(np.argmin(cum))]
        cum += L[t]
        w *= np.exp(-eta * L[t])
        hedge.append(cum_h - cum.min())
        ftl.append(cum_f - cum.min())
    return np.array(hedge), np.array(ftl)


def run(seed=0):
    lab = labs.Lab()

    # 1. PAC: the tightest box around the positives, against the rectangle bound
    ms = (20, 50, 100, 200, 500, 1000, 2000)
    rect = theory.rectangle_curves(ms=ms, trials=200, seed=seed)["rows"]
    for r in rect:
        assert r["p95"] <= r["rect_bound"], "with probability 95% the error is under (4/m) ln(4/delta)"
        if r["m"] >= 100:
            assert 2.5 < r["mean"] * r["m"] < 4.5 and r["rect_bound"] < r["vc_bound"], "the error falls like 4/m"
    for r in (rect[2], rect[-1]):
        lab.row(f"rectangle, m = {r['m']:>5}: error", f"mean {r['mean']:.4f}   95th percentile {r['p95']:.4f}   "
                f"bound (4/m) ln(4/delta) {r['rect_bound']:.4f}   VC bound {r['vc_bound']:.3f}")

    # 2. VC: half-planes on m random points, every labelling tried by a linear program
    growth = theory.growth(ms=range(1, 8), trials=1, seed=seed)
    for g in growth:
        assert g["realized"] == g["exact_general"] <= g["sauer"] <= g["all"]
    assert growth[2]["realized"] == 8 and growth[3]["realized"] < 16, "three points are shattered, four are not"
    g = growth[-1]
    lab.row(f"half-planes on {g['m']} points: labellings", f"{g['realized']} realized (m^2 - m + 2 = {g['exact_general']})"
            f"   Sauer-Shelah {g['sauer']}   all {g['all']}")

    # 3. margins: the perceptron's mistakes do not grow with the dimension
    perc = theory.perceptron_margin(dims=(2, 10, 100, 400), seed=seed)
    assert all(0 < p["mistakes"] <= p["bound"] + 1e-9 for p in perc), "Novikoff: at most (R/gamma)^2 mistakes"
    lab.row("perceptron, margin 0.1: mistakes", "   ".join(f"d = {p['d']}: {p['mistakes']}" for p in perc)
            + f"   bound (R/gamma)^2 = {perc[0]['bound']:.0f}")

    # 4. regret: Hedge under its bound on random losses and against an adversary; follow the leader is not
    h = theory.hedge(T=T_ROUNDS, N=N_EXPERTS, seed=seed)
    bound_random = math.sqrt(T_ROUNDS * math.log(N_EXPERTS) / 2)
    assert max(h["regret"]) <= bound_random
    eta = math.sqrt(8 * math.log(2) / T_ROUNDS)
    adv_hedge, adv_ftl = adversary(T_ROUNDS, eta)
    bound_adv = math.sqrt(T_ROUNDS * math.log(2) / 2)
    assert np.all(adv_hedge <= math.log(2) / eta + eta * np.arange(1, T_ROUNDS + 1) / 8) and adv_hedge.max() <= bound_adv
    assert adv_ftl[-1] > 0.45 * T_ROUNDS > 10 * bound_adv
    lab.row(f"random losses, {N_EXPERTS} experts, {T_ROUNDS} rounds: regret", f"Hedge {h['regret'][-1]:.1f}   follow the leader "
            f"{h['follow_the_leader'][-1]:.1f}   bound sqrt(T ln N / 2) = {bound_random:.1f}")
    lab.row(f"two alternating experts, {T_ROUNDS} rounds: regret", f"Hedge {adv_hedge[-1]:.1f}   follow the leader "
            f"{adv_ftl[-1]:.1f}   bound sqrt(T ln 2 / 2) = {bound_adv:.1f}")
    lab.note = ("Each bound holds with room to spare: the rectangle bound is about twice the measured quantile, the VC "
                "bound far looser, Novikoff's independent of the dimension. Only Hedge's guarantee survives an adversary.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    m = np.array([r["m"] for r in rect])
    ax[0].loglog(m, [r["vc_bound"] for r in rect], color=labs.PURPLE, label="VC bound, d = 4")
    ax[0].loglog(m, [r["rect_bound"] for r in rect], color=labs.RED, label="(4/m) ln(4/delta)")
    ax[0].loglog(m, [r["p95"] for r in rect], "o-", color=labs.GOLD, ms=4, label="measured, 95th percentile")
    ax[0].loglog(m, [r["mean"] for r in rect], "o-", color=labs.BLUE, ms=4, label="measured, mean")
    ax[0].set(title="Learning a rectangle: error against sample size", xlabel="examples m", ylabel="error")
    ax[0].legend(loc="lower left")
    t = np.arange(1, T_ROUNDS + 1)
    ax[1].plot(t, math.log(2) / eta + eta * t / 8, color=labs.RED, label="Hedge's guarantee: ln 2 / eta + eta t / 8")
    ax[1].plot(t, adv_hedge, color=labs.GREEN, label="Hedge")
    ax[1].plot(t, adv_ftl, color=labs.GOLD, label="follow the leader")
    ax[1].set(title="Regret against two alternating experts", xlabel="round t", ylabel="regret", yscale="log",
              ylim=(0.3, 2000))
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
