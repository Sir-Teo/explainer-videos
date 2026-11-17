"""Lab 14: the normal posterior and shrinkage, reliability-weighted cue combination recovered from simulated
two-interval experiments, the aperture problem solved with a slow prior, disparity's square law, retinex on a
checkerboard in shadow, and a small network that learns texture before shape."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import infer as I

TITLE = "Seeing as inference: priors, cues and a small network"
GOAL = ("Multiply a prior by a likelihood and watch the posterior shrink toward the prior as the evidence gets "
        "noisier; predict the weights and the combined precision of two cues from each cue alone, and check them with "
        "a simulated cue-conflict experiment; solve the aperture problem with a slow prior and see the percept slow "
        "and turn at low contrast; find where two eyes stop helping; take the shadow out of a checkerboard with "
        "retinex; and train a network that answers by texture until its diet changes.")
TASKS = [
    "Run the cue-combination experiment with 200, 500 and 2,000 trials a point, 50 times each. How far are the "
    "measured weights from the predicted ones, and how many trials would Ernst and Banks's four observers have needed "
    "to tell 0.6 from 0.7?",
    "Repeat the aperture problem for edges at 10 and 80 degrees, and at 40 and 50. Which pair rotates further at low "
    "contrast, and why does the angle between the edges matter?",
    "Train the network on training sets in which a fraction q of the images carry their shape's own texture. Find "
    "the q at which half the conflict answers follow texture. What does that say about how little evidence texture "
    "needs?",
]


def run(seed=0):
    out = labs.Lab()
    rng = lambda k: np.random.default_rng(seed + k)  # noqa: E731

    # 1. a posterior, and shrinkage
    m, s = I.posterior(0.0, 1.5, 4.0, 1.0)
    out.row("prior N(0, 1.5^2), measurement 4 with sd 1: posterior mean and sd", f"{m:.3f}, {s:.3f}")
    shrink = [I.posterior(0.0, 1.5, 4.0, sd)[0] for sd in (0.25, 1.0, 2.0, 4.0)]
    out.row("posterior mean as the measurement's sd grows (0.25, 1, 2, 4)", ", ".join(f"{v:.2f}" for v in shrink))
    assert all(a > b for a, b in zip(shrink, shrink[1:])), "noisier evidence moves the percept toward the prior"
    out.row("mean squared error over worlds from the prior: raw measurement vs posterior mean", f"1.000 vs {s ** 2:.3f}")

    # 2. cue combination, predicted and measured
    d = np.linspace(-14, 14, 15)
    n = 2000
    g = rng(1)
    fh = I.fit_cumulative(d, I.two_interval(4.0, d, n, g), n)
    rows = []
    for sv in (1.5, 3.0, 6.0):
        fv = I.fit_cumulative(d, I.two_interval(sv, d, n, g), n)
        _, pred_sd, w = I.combine([0, 0], [fv["sd"], fh["sd"]])
        true_w = I.combine([0, 0], [sv, 4.0])[2]
        fc = I.fit_cumulative(d, I.two_interval(None, d, n, g, weights=true_w, sds=(sv, 4.0)), n)
        fk = I.fit_cumulative(d, I.two_interval(None, d, n, g, weights=true_w, sds=(sv, 4.0), conflict=6.0), n)
        rows.append((sv, w[0], fk["pse"] / 6.0 + 0.5, pred_sd, fc["sd"]))
    for sv, wp, wo, sp, so in rows:
        out.row(f"vision sd {sv:.1f} mm, touch 4 mm: weight on vision predicted/measured; combined sd predicted/measured",
                f"{wp:.2f}/{wo:.2f}; {sp:.2f}/{so:.2f}")
        assert abs(wp - wo) < 0.08 and abs(sp - so) / sp < 0.1, "single-cue curves predict the combination"

    # 3. the aperture problem
    cons = I.edge_constraints((1.0, 0.0), (20, 60))
    for sd in (0.02, 0.3, 1.0):
        v = I.map_velocity(cons, sd)
        out.row(f"edges at 20 and 60 deg, likelihood sd {sd}: MAP direction (deg) and speed",
                f"{np.degrees(np.arctan2(v[1], v[0])):.1f}, {np.linalg.norm(v):.2f}")
    va = I.vector_average(cons)
    out.row("the vector average's direction (deg)", f"{np.degrees(np.arctan2(va[1], va[0])):.1f}")

    # 4. disparity and retinex
    out.row("disparity of 1 cm of depth at 0.5, 2 and 10 m (arcmin)",
            ", ".join(f"{I.disparity_arcmin(x, 0.01):.3f}" for x in (0.5, 2.0, 10.0)))
    cs = I.checker_shadow()
    R = I.retinex(cs["luminance"])
    out.row("checkerboard: light at A and B; retinex's surfaces at A and B",
            f"{cs['luminance'][cs['A']]:.2f}, {cs['luminance'][cs['B']]:.2f}; {R[cs['A']]:.2f}, {R[cs['B']]:.2f}")
    assert R[cs["B"]] > 1.5 * R[cs["A"]], "retinex sees the surfaces, not the light"

    # 5. a small network (short training, so the lab runs in seconds)
    X, y, _ = I.shape_texture_images(300, mode="paired", seed=seed + 1)
    net = I.TinyConvNet(seed=seed)
    loss = net.fit(X, y, steps=150, lr=0.1)
    Xt, yt, _ = I.shape_texture_images(150, mode="paired", seed=seed + 2)
    bias = I.texture_bias(net, 150, seed=seed + 99)
    out.row("network on paired images: test accuracy; conflict answers by texture / by shape",
            f"{(net.predict(Xt) == yt).mean():.2f}; {bias['texture']} / {bias['shape']}")
    out.note = ("Precisions add and means are precision-weighted, so noisy evidence leans on the prior and a biased "
                "percept can be the more accurate one. Single-cue curves predict the weights and the precision of the "
                "combination. A slow prior makes faint edges slower and turns them toward the vector average. "
                "Disparity falls with the square of distance. Retinex recovers the surfaces from the light, and a "
                "network fed paired cues learns the easy one, texture.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    x = np.linspace(-4, 8, 400)
    gauss = lambda mu, sd: np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))  # noqa: E731
    ax[0].plot(x, gauss(0, 1.5), color=labs.PINK, lw=1.6, label="prior")
    ax[0].plot(x, gauss(4, 1.0), color=labs.BLUE, lw=1.6, label="likelihood")
    ax[0].plot(x, gauss(m, s), color=labs.GREEN, lw=2.0, label="posterior")
    ax[0].set(title="A prior, a measurement, a posterior", xlabel="the quantity", ylabel="density")
    ax[0].legend(fontsize=8)
    ax[1].plot(range(len(loss)), loss, color=labs.GREEN, lw=1.6)
    ax[1].set(title="The small network's training loss", xlabel="step", ylabel="cross-entropy")
    out.fig = fig
    return out
