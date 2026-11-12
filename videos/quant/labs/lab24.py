"""Lab 24: test a factor model: all alphas zero (GRS), then one factor left out."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import factors

TITLE = "Does the model price the portfolios? The GRS test"
GOAL = ("Simulate ten test portfolios over 95 years whose returns come from three factors. Test the full model (alphas should be "
        "zero), then drop one factor and watch its premium reappear as alpha.")
TASKS = [
    "Shorten the sample to 240 months, or use 25 portfolios. Can the test still see the omitted factor?",
    "Give the third factor a premium of zero but keep the portfolios' exposure to it. Does GRS reject now?",
    "Run factors.alpha of the third factor on the first two: is it spanned?",
]


N = 10


def simulate(T, seed):
    rng = np.random.default_rng(seed)
    premia = np.array([0.005, 0.003, 0.007])  # monthly: market, value, momentum
    F = rng.normal(premia, [0.045, 0.03, 0.035], (T, 3))
    B = np.column_stack([rng.normal(1.0, 0.2, N), rng.normal(0.0, 0.5, N), rng.normal(0.0, 0.5, N)])
    R = F @ B.T + rng.normal(0, 0.02, (T, N))
    return R, F, B


def run(seed=0):
    T = 1140  # months, 1926-2020
    R, F, B = simulate(T, seed)
    full = factors.model_test(R, F)
    short = factors.model_test(R, F[:, :2])
    pvals = np.array([factors.model_test(*simulate(T, s)[:2])["p"] for s in range(1, 201)])
    lab = labs.Lab()
    lab.row("Three-factor model", f"GRS {full['grs']:.2f}, p = {full['p']:.2f}, mean |alpha| {100 * full['mean_abs_alpha']:.2f}% a year")
    lab.row("Momentum left out", f"GRS {short['grs']:.2f}, p = {short['p']:.1e}, mean |alpha| {100 * short['mean_abs_alpha']:.2f}% a year")
    lab.row("True model, 200 samples: rejected at 5%", f"{100 * np.mean(pvals < 0.05):.1f}%")
    lab.note = "An alpha is a premium for a risk the model left out, or a mistake. The test cannot say which."
    assert full["p"] > 0.01 and short["p"] < 1e-3 and 0.01 < np.mean(pvals < 0.05) < 0.11

    alphas_short = np.array([factors.alpha(R[:, i], F[:, :2])["alpha"] for i in range(N)])
    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].scatter(B[:, 2], 100 * alphas_short, color=labs.LOSS, s=22)
    slope = np.polyfit(B[:, 2], alphas_short, 1)
    xs = np.linspace(B[:, 2].min(), B[:, 2].max(), 10)
    ax[0].plot(xs, 100 * np.polyval(slope, xs), color=labs.P, ls="--", label=f"slope {100 * slope[0]:.1f}% = the premium")
    ax[0].axhline(0, color=labs.MUTED, lw=0.8)
    ax[0].set(title="Two-factor alphas line up with the missing beta", xlabel="momentum beta", ylabel="alpha, % a year")
    ax[0].legend(fontsize=8)
    ax[1].hist(pvals, bins=20, color=labs.SPOT)
    ax[1].axhline(10, color=labs.P, ls="--", lw=1)
    ax[1].set(title="GRS p-values when the model is true: uniform", xlabel="p-value")
    lab.fig = fig
    return lab
