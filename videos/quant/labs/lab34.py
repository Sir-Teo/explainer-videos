"""Lab 34: how long a seat lasts: the drawdown stop, by formula and by simulation."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import firm

TITLE = "How long does a portfolio manager's seat last?"
GOAL = ("A pod is closed when it falls a fixed number of volatilities below its peak. Compute the expected time to "
        "the stop for managers of different skill, check it by simulation, and ask what the stop selects for.")
TASKS = [
    "Halve the stop to 0.5 volatilities. How long does a Sharpe-1 manager last now, and a Sharpe-0?",
    "Use firm.platform to run 100 pods for ten years. What share of the firm's P&L comes from the top decile?",
    "A manager is stopped after three years. What is the posterior that their Sharpe ratio is above 1?",
]


def run(seed=0):
    delta = 1.0  # the stop: one annual volatility below the high-water mark
    sharpes = np.array([-0.5, 0.0, 0.5, 1.0, 1.5, 2.0])
    lab, sims = labs.Lab(), []
    # watched once a day, the peak is seen late and the breach is seen late: the stop behaves like a deeper one
    # (the Broadie-Glasserman-Kou shift of Lab 15, applied twice)
    daily = delta + 2 * 0.5826 * np.sqrt(1 / 252)
    for S in sharpes:
        out = firm.simulate_stop(S, 1.0, delta, n=3000, horizon=200.0, seed=seed)
        th = firm.stop_time_sharpe(S, delta) if S != 0 else delta ** 2
        th_daily = firm.stop_time_sharpe(S, daily) if S != 0 else daily ** 2
        sims.append(out["tau"])
        lab.row(f"Sharpe {S:+.1f}", f"expected years to the stop: formula {th:5.2f}   watched daily {th_daily:5.2f}   "
                                    f"simulated daily {out['tau']:5.2f}")
        assert out["stopped"] > 0.99 and abs(out["tau"] - th_daily) < 0.08 * th_daily + 0.03
    lab.row("Peak P&L when stopped, Sharpe 1", f"{firm.peak_at_stop(1.0, 1.0, delta):.2f} volatilities above the start")
    lab.note = ("Everyone is stopped eventually; skill only stretches the time. A zero-skill manager lasts a year, "
                "a Sharpe-2 manager six: the stop tells the two apart slowly.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    rng = np.random.default_rng(seed)
    t = np.arange(0, 6, 1 / 252)
    for i, (S, c) in enumerate(((0.0, labs.LOSS), (1.0, labs.P), (2.0, labs.GAIN))):
        for _ in range(4):
            x = np.cumsum(S / 252 + rng.standard_normal(t.size) / np.sqrt(252))
            dd = np.maximum.accumulate(x) - x
            stop = np.argmax(dd >= delta) if (dd >= delta).any() else t.size - 1
            ax[0].plot(t[:stop + 1], x[:stop + 1], color=c, lw=0.9, alpha=0.9, label=f"Sharpe {S:.0f}" if _ == 0 else None)
            if stop < t.size - 1:
                ax[0].plot(t[stop], x[stop], "x", color=c, ms=7)
    ax[0].set(title="P&L paths, closed one volatility below the peak", xlabel="years", ylabel="P&L, annual volatilities")
    ax[0].legend(fontsize=8)
    grid = np.linspace(-0.6, 2.2, 100)
    ax[1].semilogy(grid, [firm.stop_time_sharpe(s, delta) if abs(s) > 1e-9 else delta ** 2 for s in grid], color=labs.P,
                   label="(e^{2S d} - 1 - 2S d) / (2 S^2)")
    ax[1].semilogy(sharpes, sims, "o", color=labs.SPOT, label="simulated")
    ax[1].set(title="Expected years until the stop", xlabel="the manager's true Sharpe ratio")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
