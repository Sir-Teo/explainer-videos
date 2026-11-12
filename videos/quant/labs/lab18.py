"""Lab 18: duration and convexity, and why every curve moves in level, slope and curvature."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import rates

TITLE = "Duration, convexity, and three factors from one assumption"
GOAL = ("Reprice a ten-year bond for shifts of up to two points against its duration and convexity "
        "approximations. Then simulate curve changes whose only structure is that nearby maturities move "
        "together, and let principal components find level, slope and curvature.")
TASKS = [
    "Build a duration-neutral 2s5s10s butterfly with rates.fly_weights and check its exposure to the first two factors.",
    "Lower the correlation decay so neighbours are less alike. What happens to the first component's share?",
    "Compare the 30-year zero's convexity with the 30-year par bond's. Which gains more from volatile rates?",
]


def run(seed=0):
    coupon, y, T = 0.04, 0.04, 10
    risk = rates.bond_risk(coupon, y, T)
    shifts = np.linspace(-0.02, 0.02, 81)
    exact = np.array([rates.bond_price(coupon, y + s, T) for s in shifts])
    dur = risk["price"] * (1 - risk["modified"] * shifts)
    conv = dur + 0.5 * risk["price"] * risk["convexity"] * shifts ** 2
    lab = labs.Lab()
    lab.row("10-year 4% bond at par", f"modified duration {risk['modified']:.2f}, convexity {risk['convexity']:.1f}, "
                                      f"DV01 {risk['dv01']:.4f} per 100")
    lab.row("Rates +200 bp: exact / duration / + convexity", f"{exact[-1]:.2f} / {dur[-1]:.2f} / {conv[-1]:.2f}")
    lab.row("Rates -200 bp: exact / duration / + convexity", f"{exact[0]:.2f} / {dur[0]:.2f} / {conv[0]:.2f}")
    assert abs(conv[-1] - exact[-1]) < 0.2 < abs(dur[-1] - exact[-1]) and (exact >= dur - 1e-9).all()

    mats = np.array([0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
    # nearby maturities are alike: correlation falls with the distance in log maturity
    corr = np.exp(-0.35 * np.abs(np.log(mats)[:, None] - np.log(mats)[None, :]))
    rng = np.random.default_rng(seed)
    dy = rng.multivariate_normal(np.zeros(len(mats)), 0.06 ** 2 * corr, size=5000)
    pca = rates.curve_pca(dy)
    changes = [int(np.sum(np.diff(np.sign(v)) != 0)) for v in pca["loadings"][:3]]
    lab.row("Variance explained by 3 components", "  ".join(f"{100 * s:.1f}%" for s in pca["share"][:3]))
    lab.row("Sign changes of the loadings", f"{changes}   (level 0, slope 1, curvature 2)")
    lab.note = ("No economics was put in: a correlation that decays with distance is totally positive, and such "
                "matrices have eigenvectors with 0, 1, 2, ... sign changes (Gantmacher and Krein).")
    assert changes == [0, 1, 2] and pca["share"][0] > 0.6

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(1e4 * shifts, exact, color=labs.INK, lw=2.4, label="exact price")
    ax[0].plot(1e4 * shifts, dur, color=labs.LOSS, ls="--", label="duration only")
    ax[0].plot(1e4 * shifts, conv, color=labs.GAIN, ls=":", lw=2, label="duration + convexity")
    ax[0].set(title="A ten-year bond against a parallel shift", xlabel="shift in yield, bp", ylabel="price per 100")
    ax[0].legend()
    for v, c, name in zip(pca["loadings"][:3], (labs.P, labs.SPOT, labs.OPTION), ("level", "slope", "curvature")):
        ax[1].plot(np.arange(len(mats)), v, "o-", color=c, label=name)
    ax[1].axhline(0, color=labs.MUTED, lw=0.8)
    ax[1].set_xticks(np.arange(len(mats)), [f"{m:g}" for m in mats])
    ax[1].set(title="Principal components of simulated curve changes", xlabel="maturity, years")
    ax[1].legend()
    lab.fig = fig
    return lab
