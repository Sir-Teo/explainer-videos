"""Lab 41: audit a calibrated risk score in two groups, and see what noise does and does not protect."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import fairness

TITLE = "A calibrated score that cannot be balanced, and a count that can be private"
GOAL = ("Draw two groups with base rates 30% and 50% and a perfectly calibrated score. Check Chouldechova's identity "
        "and Kleinberg's four-line identity in each group, try to equalize error rates or precision with group "
        "thresholds, then check randomized response, the reconstruction attack and the Shapley values' sum.")
TASKS = [
    "Call fairness.population with means=(0.4, 0.4). Which of the gaps between the groups at threshold 0.5 "
    "disappear, and which remain as sampling noise?",
    "In fairness.reconstruction ask only n queries instead of 4n (edit m). How much noise is now enough to protect "
    "the secret bits?",
    "Change the randomized-response coin so that people answer truthfully with probability 3/4. Derive the new "
    "estimator and epsilon, and compare the standard error.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    s = 2016 + seed

    c = fairness.criteria(t=0.5, seed=s)
    ra, rb = c["rates"]["A"], c["rates"]["B"]
    lab.row("one threshold at 0.5: false-positive rate A, B", f"{ra['fpr']:.3f}, {rb['fpr']:.3f}   (film: about 0.10 and 0.30)")
    lab.row("... precision A, B", f"{ra['ppv']:.3f}, {rb['ppv']:.3f}")
    for g in "AB":
        r = c["rates"][g]
        assert abs(c["identity_fpr"][g] - r["fpr"]) < 2e-3, "Chouldechova's identity reproduces the FPR"
    assert abs(ra["fpr"] - 0.10) < 0.02 and abs(rb["fpr"] - 0.30) < 0.03 and rb["fpr"] > 2.5 * ra["fpr"]

    odds, rhs = {}, {}
    for g in "AB":
        p, x, y = c["rates"][g]["base"], c["balance"][g]["pos"], c["balance"][g]["neg"]
        odds[g], rhs[g] = p / (1 - p), y / (1 - x)
        assert abs(odds[g] - rhs[g]) < 0.06 * odds[g], "calibration forces p/(1-p) = y/(1-x) in each group"
    lab.row("base-rate odds p/(1-p), A and B", f"{odds['A']:.2f}, {odds['B']:.2f}   (film: 0.42, 1.02)")
    lab.row("y/(1-x) from the class-average scores", f"{rhs['A']:.2f}, {rhs['B']:.2f}   (film: 0.43, 0.99)")
    assert c["balance"]["B"]["pos"] - c["balance"]["A"]["pos"] > 0.1, "so the class averages cannot match"
    assert c["balance"]["B"]["neg"] - c["balance"]["A"]["neg"] > 0.1

    sw = fairness.sweep(seed=s)
    gap = [b["fpr"] - a["fpr"] for a, b in zip(sw["rates"]["A"], sw["rates"]["B"])]
    lab.row("least FPR gap (B minus A) over 17 shared thresholds", f"{min(gap):+.3f}   (never zero)")
    assert min(gap) > 0, "no shared threshold equalizes the false-positive rates"
    gt = fairness.group_thresholds(seed=s)
    eq_fpr, eq_ppv = gt["fpr"], gt["ppv"]
    lab.row("group thresholds with equal FPR: precision A, B", f"{eq_fpr['A']['ppv']:.3f}, {eq_fpr['B']['ppv']:.3f}")
    lab.row("group thresholds with equal precision: FPR A, B", f"{eq_ppv['A']['fpr']:.3f}, {eq_ppv['B']['fpr']:.3f}")
    assert abs(eq_fpr["A"]["fpr"] - eq_fpr["B"]["fpr"]) < 0.01 and eq_fpr["B"]["ppv"] - eq_fpr["A"]["ppv"] > 0.1
    assert abs(eq_ppv["A"]["ppv"] - eq_ppv["B"]["ppv"]) < 0.01 and eq_ppv["B"]["fpr"] - eq_ppv["A"]["fpr"] > 0.15

    for m in fairness.laplace()["mechanisms"]:
        assert abs(m["max_ratio"] - math.exp(m["eps"])) < 1e-3, "the Laplace mechanism's worst ratio is e^eps"
    rr = fairness.randomized_response(n=20000, seed=1965 + seed)
    lab.row("randomized response, 20,000 people, true share 0.30", f"estimate {rr['estimate']:.3f} +/- {rr['se']:.3f}   (eps = ln 3)")
    assert abs(rr["estimate"] - rr["sample_true"]) < 4 * rr["se"] and abs(rr["eps"] - math.log(3)) < 1e-4
    rec = fairness.reconstruction(seed=2003 + seed)
    got = {r["noise"]: r["recovered"] for r in rec["results"]}
    lab.row("secret bits rebuilt from noisy sums: noise 1, 4, 16", f"{got[1.0]:.0%}, {got[4.0]:.0%}, {got[16.0]:.0%}   (sqrt(n) = {rec['sqrt_n']:.0f})")
    assert got[0.0] == 1.0 and got[1.0] > 0.97 and got[16.0] < got[1.0] - 0.15, "small noise protects nothing"

    x = tuple(np.round(rng.uniform(0.2, 2.0, 3), 2))
    ex = fairness.explain(x=x)
    inc, hist, debt = x
    by_hand = [0.4 * inc + 0.1 * inc * hist, 0.3 * hist + 0.1 * inc * hist, -0.5 * debt]
    lab.row(f"Shapley values at income, history, debt = {inc}, {hist}, {debt}", ", ".join(f"{p:+.3f}" for p in ex["phi"]))
    assert ex["sum_ok"] and np.allclose(ex["phi"], by_hand, atol=1e-3), "the interaction is split equally"
    lab.note = ("The score treats everyone alike and is calibrated in both groups, yet with unequal base rates no "
                "threshold policy equalizes error rates and precision together: which gap to accept is a moral "
                "choice. Noise protects a count only when it is large compared with the square root of the data.")

    fig, ax = labs.figure(2, size=(11.5, 4.3))
    ts = sw["ts"]
    for g, color in (("A", labs.BLUE), ("B", labs.ORANGE)):
        ax[0].plot(ts, [r["fpr"] for r in sw["rates"][g]], color=color, label=f"group {g}: false-positive rate")
        ax[0].plot(ts, [r["ppv"] for r in sw["rates"][g]], color=color, ls="--", label=f"group {g}: precision")
    ax[0].axvline(0.5, color=labs.MUTED, ls=":", lw=1)
    ax[0].set(title="One threshold for two calibrated groups", xlabel="threshold on the score", ylabel="rate", ylim=(0, 1.3),
              yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[0].legend(loc="upper center", ncol=2, fontsize=8)
    noise = [r["noise"] for r in rec["results"]]
    xs = np.arange(len(noise))
    hit = np.array([got[e] > 0.9 for e in noise])
    ax[1].set_axisbelow(True)
    ax[1].bar(xs[hit], [got[e] for e in np.array(noise)[hit]], color=labs.RED, label="over 90% rebuilt")
    ax[1].bar(xs[~hit], [got[e] for e in np.array(noise)[~hit]], color=labs.BLUE, label="under 90%")
    ax[1].axhline(0.5, color=labs.INK, ls="--", lw=1, label="guessing")
    ax[1].set(title="Rebuilding 64 secret bits from 256 noisy sums", xticks=xs, xticklabels=[f"{e:g}" for e in noise],
              xlabel="size of the noise added to each answer", ylabel="share of bits recovered", ylim=(0, 1.3),
              yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[1].legend(loc="upper center", ncol=3)
    lab.fig = fig
    return lab
