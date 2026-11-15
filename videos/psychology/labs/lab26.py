"""Lab 26: prospect theory computed (Allais, the disease problem, the fourfold pattern) and fitted to choices13k
against expected value out of sample; take-the-best against regression; the hot-hand bias by exact enumeration."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import choice as C

TITLE = "Judgment and choice"
GOAL = ("Compute prospect theory's verdicts on Allais's problems and the disease problem; fit it to 1,928 open "
        "choice problems and test it on problems held out; pit a one-cue rule against regression; and count the "
        "bias hidden in the hot-hand test.")
TASKS = [
    "Refit choices13k with Prelec's weighting function (C.w_prelec) in place of C.w_tk, separately for gains and "
    "losses. Does it predict held-out problems better, and what happens to loss aversion?",
    "Lower the noise in the non-compensatory world from 3 to 1. Up to how many training objects does take-the-best "
    "still beat regression?",
    "Compute the expected hit rate after streaks of one, two and three hits for a 50% shooter taking 100 shots. How "
    "large a hot hand could a finding of 'no difference' hide?",
]


def run(seed=0):
    out = labs.Lab()

    # 1. prospect theory computed
    A = C.lottery((0.33, 2500), (0.66, 2400), (0.01, 0))
    B = C.lottery((1.0, 2400))
    Cc = C.lottery((0.33, 2500), (0.67, 0))
    D = C.lottery((0.34, 2400), (0.66, 0))
    v = {k: C.cpt(L) for k, L in zip("ABCD", (A, B, Cc, D))}
    out.row("Allais with the 1992 values: problem 1, problem 2",
            f"{'B' if v['B'] > v['A'] else 'A'}, {'C' if v['C'] > v['D'] else 'D'}")
    for u, name in ((np.sqrt, "sqrt"), (np.log1p, "log")):
        out.row(f"EU({name}): A - B and C - D (always equal)",
                f"{C.eu(A, u) - C.eu(B, u):.4f}, {C.eu(Cc, u) - C.eu(D, u):.4f}")
    assert v["B"] > v["A"] and v["C"] > v["D"]
    fr = C.framing()
    out.row("disease problem: choice when saved, when dying", f"{fr['saved_choice']}, {fr['die_choice']}")
    ff = C.fourfold(probs=(0.05, 0.95))
    out.row("certainty equivalents of 100 at 5%, 95%", f"{ff['gain_ce'][0]:.1f}, {ff['gain_ce'][1]:.1f}")
    out.row("certainty equivalents of -100 at 5%, 95%", f"{ff['loss_ce'][0]:.1f}, {ff['loss_ce'][1]:.1f}")

    # 2. choices13k
    d = opendata.choices13k()
    sel = np.where(~d["amb"] & ~d["feedback"])[0]
    Ap = C.pad([d["A"][i] for i in sel])
    Bp = C.pad([d["B"][i] for i in sel])
    y = d["b_rate"][sel]
    fit = C.fit_model("cpt", Ap, Bp, y)
    p = fit["params"]
    out.row("described problems; variance of the B rate", f"{len(sel)}; {y.var():.4f}")
    out.row("prospect theory fitted: alpha, lambda, gamma, delta",
            f"{p['alpha']:.2f}, {p['lam']:.2f}, {p['gamma']:.2f}, {p['delta']:.2f}")
    cv = C.cv_models(Ap, Bp, y, models=("ev", "cpt"), k=5, seed=seed)
    assert cv["cpt"] < cv["ev"] < cv["mean"]
    out.row("5-fold cross-validated MSE: mean, EV, prospect theory",
            f"{cv['mean']:.4f}, {cv['ev']:.4f}, {cv['cpt']:.4f}")

    # 3. take-the-best
    r = C.heuristics_cv((8, 4, 2, 1, 0.5, 0.25), (8, 15, 40, 80), reps=60, noise=3.0, seed=seed)
    out.row("accuracy with 8, 15, 40, 80 objects: take-the-best",
            ", ".join(f"{x:.3f}" for x in r["ttb"]))
    out.row("the same: regression", ", ".join(f"{x:.3f}" for x in r["regression"]))

    # 4. the hot hand
    ns = np.arange(3, 17)
    bias = np.array([C.streak_exact(int(n), 1)["expected"] for n in ns])
    assert abs(C.streak_exact(4, 1)["expected"] - 17 / 42) < 1e-12
    out.row("expected share of heads after a head, 4 flips (17/42)", f"{C.streak_exact(4, 1)['expected']:.4f}")
    out.row("100 shots, after three hits (simulated)",
            f"{C.streak_sim(100, 3, reps=50_000, seed=seed)['expected']:.3f}")

    out.note = ("Prospect theory makes the popular Allais and framing choices; on open data it beats expected value "
                "out of sample, with loss aversion near one at these stakes; a one-cue rule beats regression when "
                "data are scarce; and the hot-hand test was biased toward finding nothing.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    pr = C.predict("cpt", fit["theta"], Ap, Bp)
    ax[0].scatter(pr[::3], y[::3], s=6, color=labs.BLUE, alpha=0.6)
    ax[0].plot([0, 1], [0, 1], ls="--", color="#888888")
    ax[0].set(title="choices13k: prospect theory", xlabel="predicted share choosing B", ylabel="observed")
    ax[1].plot(ns, bias, marker="o", color=labs.GOLD)
    ax[1].axhline(0.5, ls="--", color="#888888")
    ax[1].set(title="The streak statistic's bias", xlabel="flips", ylabel="expected share after a head")
    out.fig = fig
    return out
