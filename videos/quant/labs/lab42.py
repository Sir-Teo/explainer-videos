"""Lab 42: herding makes fat tails: Kirman's ants, and a market of fundamentalists and chartists."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import agents

TITLE = "Herding and the stylized facts"
GOAL = ("A hundred traders hold one of two views and convert each other at random. Simulate the share holding "
        "each view and compare it with the exact stationary law as the rate of independent switching falls. Then "
        "run a market of fundamentalists and chartists and measure its tails and its volatility clustering.")
TASKS = [
    "Find the critical eps at which the stationary law turns from one hump to two (it depends on N).",
    "In agents.fw_model, switch herding off (a_n = 0). Which stylized fact disappears first?",
    "Give every trader the same forecasting model (agents.crowd). What does a shared error do to volatility?",
]


def run(seed=0):
    N, delta, T = 100, 0.3, 400000
    lab, sims = labs.Lab(), {}
    for eps in (0.0005, 0.1):
        k = agents.kirman(N, eps, delta, T, seed=seed)
        emp = np.bincount(k[T // 20:], minlength=N + 1) / (T - T // 20)
        th = agents.kirman_stationary(N, eps, delta)
        sims[eps] = (k, emp, th)
        ends = emp[:11].sum() + emp[-11:].sum()
        lab.row(f"eps = {eps}", f"time with more than 90% on one side: simulated {100 * ends:.0f}%, exact "
                                f"{100 * (th[:11].sum() + th[-11:].sum()):.0f}%")
    out = agents.fw_model(T=40000, seed=seed)
    st = agents.stylized(out["r"])
    lab.row("Fundamentalists and chartists", f"excess kurtosis {st['kurt']:.1f}, tail exponent {st['hill']:.1f}, "
                                             f"autocorrelation of |r| at lag 1: {st['acf_abs'][0]:.2f}, of r: {st['acf_r'][0]:+.2f}")
    lab.note = ("No news arrives in either model. Fat tails and volatility clusters come from traders copying "
                "each other; returns stay unpredictable.")
    lo, hi = sims[0.0005], sims[0.1]
    assert lo[2][0] > lo[2][50] and hi[2][50] > hi[2][0], "herding: two humps; independence: one"
    assert abs((hi[1] * np.arange(N + 1)).sum() - 50) < 3 and st["kurt"] > 1 and st["acf_abs"][0] > 0.1 > abs(st["acf_r"][0])

    fig, ax = labs.figure(3, size=(12, 3.9))
    step = 200
    ax[0].plot(np.arange(0, T, step) / 1e3, lo[0][::step], color=labs.LOSS, lw=0.7, label="eps = 0.0005")
    ax[0].plot(np.arange(0, T, step) / 1e3, hi[0][::step], color=labs.SPOT, lw=0.7, label="eps = 0.1")
    ax[0].set(title="Traders holding view A", xlabel="thousand meetings", ylabel="of 100")
    ax[0].legend(fontsize=8)
    kk = np.arange(N + 1)
    for (k, emp, th), c in ((lo, labs.LOSS), (hi, labs.SPOT)):
        ax[1].bar(kk, emp, width=1.0, color=c, alpha=0.4)
        ax[1].plot(kk, th, color=c)
    ax[1].set(title="Time spent at each share: simulation and exact law", xlabel="traders holding view A", ylim=(0, 0.06))
    ax[2].plot(100 * out["r"][:6000], color=labs.SPOT, lw=0.4)
    ax[2].set(title="Returns of the two-type market", xlabel="period", ylabel="%")
    lab.fig = fig
    return lab
