"""Lab 21: the exposure of a swap, what collateral removes, and the CVA that is left."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import rates, termstructure, xva

TITLE = "Exposure, collateral and CVA on one swap"
GOAL = ("Simulate a ten-year payer swap under Hull-White, draw its expected and potential future exposure, add "
        "daily variation margin with a ten-day margin period of risk, and price the counterparty's default.")
TASKS = [
    "Make it a receiver swap (payer=False). Why is the exposure profile not the mirror image?",
    "Raise the threshold from 0 to 2% of notional. How much CVA comes back?",
    "Double the counterparty's hazard rate, then make exposure rise with it (xva.wrong_way_cva).",
]


def run(seed=0):
    curve = rates.Curve(np.array([0.5, 1, 2, 5, 10, 30]), np.array([0.030, 0.031, 0.033, 0.036, 0.038, 0.040]))
    hw = termstructure.HullWhite(curve, a=0.05, sigma=0.01)
    T_end = 10.0
    K = curve.par(T_end, freq=1)
    times = np.linspace(0, T_end, 241)[1:]  # twice a month
    x, _ = hw.simulate_x(times, 20000, seed=seed)
    V = np.column_stack([xva.swap_values_hw(hw, x[:, i], t, K, T_end, freq=1, notional=100.0, payer=True)
                         for i, t in enumerate(times)])
    raw = xva.exposure_profile(V)
    coll = xva.exposure_profile(xva.collateralised(V, times, threshold=0.0, mpor=10 / 252))
    knots, hazards = np.array([10.0]), np.array([0.02])  # a flat 2% hazard: about a 120 bp spread at 40% recovery
    cva_raw = xva.cva(raw["EE"], times, curve.df, knots, hazards, R=0.4)
    cva_coll = xva.cva(coll["EE"], times, curve.df, knots, hazards, R=0.4)
    annuity = sum(curve.df(t) for t in range(1, 11))
    lab = labs.Lab()
    lab.row("Par swap rate", f"{100 * K:.3f}%")
    lab.row("Peak expected exposure", f"{raw['EE'].max():.2f} per 100 notional, at year {times[raw['EE'].argmax()]:.1f}")
    lab.row("Peak 95% potential future exposure", f"{raw['PFE'].max():.2f}")
    lab.row("CVA, uncollateralised", f"{cva_raw:.3f} per 100  =  {1e4 * cva_raw / (100 * annuity):.1f} bp running")
    lab.row("CVA, daily margin, 10-day MPoR", f"{cva_coll:.3f} per 100  ({100 * cva_coll / cva_raw:.0f}% of the above)")
    lab.note = "Collateral leaves only what the swap can move in the ten days it takes to close out a defaulter."
    assert abs(V[:, 0].mean()) < 0.3 and 0 < cva_coll < 0.25 * cva_raw and 2 < times[raw["EE"].argmax()] < 6
    assert raw["EE"][-1] < 0.2 * raw["EE"].max(), "exposure dies as the swap amortises"

    fig, ax = labs.figure(2, size=(11, 4.2))
    for path in V[:60]:
        ax[0].plot(times, path, color=labs.SPOT, lw=0.5, alpha=0.5)
    ax[0].axhline(0, color=labs.MUTED, lw=0.8)
    ax[0].set(title="Value of a 10-year payer swap on 60 paths", xlabel="years", ylabel="per 100 notional")
    ax[1].fill_between(times, raw["EE"], color=labs.LOSS, alpha=0.3)
    ax[1].plot(times, raw["EE"], color=labs.LOSS, label="expected exposure")
    ax[1].plot(times, raw["PFE"], color=labs.P, ls="--", label="95% potential future exposure")
    ax[1].plot(times, coll["EE"], color=labs.GAIN, label="expected exposure with margin")
    ax[1].set(title="Exposure profiles", xlabel="years")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
