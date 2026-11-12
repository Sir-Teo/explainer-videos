"""Lab 35: the spread as insurance against the informed, and prices that learn from orders."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import micro

TITLE = "Why there is a spread: Glosten-Milgrom and Kyle"
GOAL = ("A dealer cannot tell informed traders from noise. Compute the zero-profit bid and ask as the informed "
        "share grows, watch the dealer's belief converge on the truth trade by trade, then run Kyle's insider "
        "in continuous time and check that prices reveal the value exactly at the end.")
TASKS = [
    "Start the dealer's prior at 0.9 instead of 0.5. Where is the spread widest, and why?",
    "In micro.kyle_one, double the noise traders' volume. What happens to lambda and to the insider's profit?",
    "Estimate Roll's spread (micro.roll_spread) from the simulated trade prices. Why is it below the quoted one?",
]


def run(seed=0):
    lab = labs.Lab()
    mus = np.linspace(0.0, 0.9, 46)
    spreads = np.array([np.subtract(*micro.gm_quotes(0.5, m)) for m in mus])
    for m in (0.1, 0.3, 0.5):
        ask, bid = micro.gm_quotes(0.5, m)
        lab.row(f"Informed share {m:.0%}", f"bid {bid:.3f}, ask {ask:.3f}: spread {ask - bid:.3f}")
        assert abs((ask - bid) - m) < 1e-9, "at a prior of one half the spread equals the informed share"
    run_ = micro.gm_simulate(0.3, 200, v_true=1.0, p0=0.5, seed=seed)
    half_life = int(np.argmax(run_["p"] > 0.99))
    lab.row("Belief passes 99% after", f"{half_life} trades (30% informed, true value high)")
    k1 = micro.kyle_one(sigma_v=1.0, sigma_u=1.0)
    lab.row("Kyle, one auction", f"lambda {k1['lambda']:.2f}, insider profit {k1['profit']:.2f}, variance revealed "
                                 f"{100 * (1 - k1['post_var']):.0f}%")
    ends = [micro.kyle_continuous(v, 0.0, 1.0, 1.0, n=2000, seed=seed + i) for i, v in enumerate((1.2, -0.7, 0.4))]
    gaps = [abs(e["p"][-1] - v) for e, v in zip(ends, (1.2, -0.7, 0.4))]
    lab.row("Kyle, continuous: |final price - value|", "  ".join(f"{g:.3f}" for g in gaps))
    lab.note = ("The spread is what uninformed traders pay so the dealer breaks even against informed ones. "
                "Order flow moves prices because it might be informed.")
    assert run_["p"][-1] > 0.99 and max(gaps) < 0.08 and np.all(np.diff(spreads) >= -1e-12)

    fig, ax = labs.figure(3, size=(12, 3.9))
    ax[0].plot(100 * mus, spreads, color=labs.P)
    ax[0].set(title="Zero-profit spread", xlabel="informed traders, %", ylabel="ask - bid (value is 0 or 1)")
    n = np.arange(len(run_["p"]))
    ax[1].fill_between(n[:120], run_["bid"][:120], run_["ask"][:120], color=labs.SPOT, alpha=0.3, label="bid to ask")
    ax[1].plot(n[:120], run_["p"][:120], color=labs.SPOT, label="dealer's belief")
    ax[1].axhline(1.0, color=labs.GAIN, ls="--", lw=1)
    ax[1].set(title="Learning from the tape", xlabel="trade")
    ax[1].legend(fontsize=8)
    for e, v, c in zip(ends, (1.2, -0.7, 0.4), (labs.GAIN, labs.LOSS, labs.P)):
        ax[2].plot(e["t"], e["p"], color=c, lw=0.9)
        ax[2].plot(1.0, v, "o", color=c)
    ax[2].set(title="Kyle: the price is a bridge to the value", xlabel="time")
    lab.fig = fig
    return lab
