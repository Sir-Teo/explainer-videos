"""Lab 56: check Cheeger's inequality against every cut of small graphs, and a walk's mixing against the spectral gap."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import math

import numpy as np

from explainer.cs.spectral import spectra

TITLE = "What the second eigenvalue promises: cuts, walks and expanders"
GOAL = ("On random 12-vertex graphs compare the best conductance over all 2,047 cuts with lambda_2 / 2 and "
        "sqrt(2 lambda_2) and with the sweep cut; on four 64-vertex graphs compare the lazy walk's distance from "
        "stationarity with the spectral bound; and measure random regular graphs against 2 sqrt(d - 1).")
TASKS = [
    "Replace the 12-vertex random graphs by spectra.cycle(12) and by the hypercube Q_3 with a pendant path. Which side of Cheeger's inequality does each come close to?",
    "Add spectra.barbell(32) with 2,000 steps to the mixing panel. Which vertex set is the bottleneck, and how does its conductance compare with the gap?",
    "Build spectra.zigzag(G, H) for a random 8-regular G on 60 vertices and a random 3-regular H on 8, and compare its second eigenvalue with 1 - (1 - lambda_H)^2 (1 - lambda_G).",
]

N = 64


def worst_start(A, steps):
    """The lazy walk's total-variation distance from stationarity, maximized over the starting vertex, per step."""
    d = A.sum(axis=1)
    W = 0.5 * (np.eye(len(A)) + A / d[:, None])
    pi = d / d.sum()
    P, out = np.eye(len(A)), []
    for _ in range(steps + 1):
        out.append(float(0.5 * np.abs(P - pi).sum(axis=1).max()))
        P = P @ W
    return np.array(out), pi


def run(seed=0):
    lab = labs.Lab()

    # 1. Cheeger on graphs small enough to try every cut
    rows = spectra.cheeger_check(trials=24, seed=seed)
    assert len(rows) >= 12
    for r in rows:
        assert r["lower"] - 1e-9 <= r["phi"] <= r["sweep"] + 1e-9 <= r["upper"] + 2e-9, "lambda2/2 <= phi <= sweep <= sqrt(2 lambda2)"
    exact = sum(abs(r["sweep"] - r["phi"]) < 1e-9 for r in rows)
    tight = min(rows, key=lambda r: r["phi"] / r["lower"])
    lab.row(f"{len(rows)} connected random graphs on 12 vertices", f"all inside lambda2/2 <= phi <= sqrt(2 lambda2); "
            f"the sweep cut is the best cut in {exact}")
    lab.row("closest to the lower bound", f"phi = {tight['phi']:.3f} against lambda2/2 = {tight['lower']:.3f} "
            f"and sqrt(2 lambda2) = {tight['upper']:.3f}")

    # 2. the lazy walk against the gap, from the worst starting vertex
    graphs = {"random 4-regular": (spectra.random_regular(N, 4, seed=seed + 1), 80),
              "8 x 8 grid": (spectra.grid(8, 8), 250), "cycle": (spectra.cycle(N), 1400)}
    curves = {}
    for name, (A, steps) in graphs.items():
        gap = float(np.linalg.eigvalsh(spectra.laplacian(A, True))[1])
        tv, pi = worst_start(A, steps)
        bound = 0.5 * math.sqrt(1 / pi.min()) * (1 - gap / 2) ** np.arange(steps + 1)
        t_mix = int(np.argmax(tv < 0.25))
        lo, hi = (2 / gap - 1) * math.log(2), math.log(4 / pi.min()) / gap
        assert tv[t_mix] < 0.25 and np.all(tv <= bound + 1e-12), "the walk is under the spectral bound at every step"
        assert lo <= t_mix <= hi, "the mixing time lies between the two bounds the gap gives"
        curves[name] = (tv, bound)
        lab.row(f"{name}: gap {gap:.4f}", f"t_mix = {t_mix}   (bounds from the gap: {lo:.0f} to {hi:.0f})")

    # 3. random regular graphs against the Alon-Boppana limit
    spec = spectra.regular_spectra(n=200, ds=(3, 4, 8), seed=seed)
    for r in spec:
        assert abs(r["lambda"] / r["ramanujan"] - 1) < 0.08 and r["mixing_worst"] <= r["lambda"] + 1e-9
        lab.row(f"random {r['d']}-regular graph on 200 vertices", f"lambda = {r['lambda']:.3f}   2 sqrt(d - 1) = "
                f"{r['ramanujan']:.3f}   worst mixing-lemma error {r['mixing_worst']:.2f} (at most lambda)")
    lab.note = ("The second eigenvalue brackets the best cut from both sides, sets how fast a walk mixes, and for a "
                "random regular graph sits near 2 sqrt(d - 1), as small as any large d-regular graph allows.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    lam = np.linspace(0.001, max(r["lambda2"] for r in rows) * 1.08, 200)
    ax[0].plot(lam, np.sqrt(2 * lam), color=labs.RED, label="sqrt(2 lambda2)")
    ax[0].plot(lam, lam / 2, color=labs.GREEN, label="lambda2 / 2")
    ax[0].scatter([r["lambda2"] for r in rows], [r["sweep"] for r in rows], s=34, facecolors="none",
                  edgecolors=labs.GOLD, label="sweep cut")
    ax[0].scatter([r["lambda2"] for r in rows], [r["phi"] for r in rows], s=12, color=labs.BLUE, label="best of all 2,047 cuts")
    ax[0].set(title="Cheeger's inequality on random 12-vertex graphs", xlabel="lambda2 of the normalized Laplacian",
              ylabel="conductance")
    ax[0].legend(loc="upper left")
    for (name, (tv, bound)), color in zip(curves.items(), (labs.BLUE, labs.GOLD, labs.PURPLE)):
        t = np.arange(len(tv))
        ax[1].loglog(t[1:], tv[1:], color=color, label=name)
        ax[1].loglog(t[1:], np.minimum(bound[1:], 1), color=color, ls="--", lw=1)
    ax[1].axhline(0.25, color=labs.MUTED, lw=1, ls=":")
    ax[1].text(1.1, 0.27, "1/4: mixed", color=labs.MUTED, fontsize=9)
    ax[1].set(title="Lazy walks: distance (solid) and bound (dashed)", xlabel="steps",
              ylabel="total variation, worst start", ylim=(1e-3, 1.5))
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab
