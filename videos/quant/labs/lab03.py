"""Lab 3: a discounted cash flow, its duration, and the rate the price implies."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import valuation

TITLE = "A DCF, its duration, and the rate a price implies"
GOAL = ("Value five years of free cash flow plus a terminal value; show how much of the value is terminal, how "
        "sensitive it is to the discount rate, and back out the rate a market price implies.")
TASKS = [
    "Lower the discount rate from 8% to 6%. By how much does the value rise, and what did duration predict?",
    "Replace the Gordon terminal value with valuation.value_driver_tv at RONIC = WACC. What does growth add now?",
    "Use valuation.residual_income on the same firm and check that it returns the DCF value.",
]


def run(seed=0):
    fcf = 100 * 1.08 ** np.arange(1, 6)  # five years of free cash flow growing 8%
    r, g = 0.08, 0.03
    v = valuation.dcf(fcf, r, g)
    dur = valuation.gordon_duration(r, g)
    bump = 1e-4
    numeric = -(np.log(valuation.gordon(1, r + bump, g)) - np.log(valuation.gordon(1, r - bump, g))) / (2 * bump)
    implied = valuation.implied_rate(price=v["value"], cf0=100, growth=0.08, growth_long=g, years=5)
    lab = labs.Lab()
    lab.row("DCF value", f"{v['value']:,.0f}   explicit years {v['explicit']:,.0f}, terminal {v['terminal']:,.0f} "
                         f"({100 * v['terminal'] / v['value']:.0f}%)")
    lab.row("Gordon duration at r=8%, g=3%", f"modified {dur['modified']:.1f} years (numerical {numeric:.1f}), "
                                             f"Macaulay {dur['macaulay']:.1f}")
    lab.row("Rate implied by that price", f"{100 * implied:.2f}%")
    lab.note = "A stock is a long bond: one point on the discount rate moves this value by about a fifth."
    assert abs(numeric - dur["modified"]) < 1e-3 and abs(implied - r) < 1e-6 and v["terminal"] > v["explicit"]

    rates = np.linspace(0.05, 0.12, 60)
    fig, ax = labs.figure(2, size=(11, 4.2))
    for gg, c in ((0.01, labs.CASH), (0.03, labs.P), (0.04, labs.LOSS)):
        ax[0].plot(100 * rates, [valuation.dcf(fcf, x, gg)["value"] for x in rates], color=c, label=f"g = {gg:.0%}")
    ax[0].plot(100 * r, v["value"], "o", color=labs.P)
    ax[0].set(title="Value against the discount rate", xlabel="discount rate, %", ylabel="value", ylim=(0, 9000))
    ax[0].legend()
    years = np.arange(1, 61)
    w = valuation.pv_weights(r, g, 60)
    ax[1].bar(years, 100 * np.asarray(w)[:60], color=labs.SPOT)
    ax[1].axvline(dur["macaulay"], color=labs.P, ls="--")
    ax[1].text(dur["macaulay"] + 1, ax[1].get_ylim()[1] * 0.9, f"mean date {dur['macaulay']:.0f} y", color=labs.P)
    ax[1].set(title="Where the value sits in time", xlabel="year of payment", ylabel="% of value")
    lab.fig = fig
    return lab
