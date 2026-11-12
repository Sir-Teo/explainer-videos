"""Lab 37: how to sell a large position: Almgren-Chriss, and a book that recovers."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import execution

TITLE = "Optimal execution: urgency against impact"
GOAL = ("Liquidate a position over one day. Trace Almgren and Chriss's schedules and their cost-risk frontier as "
        "risk aversion grows; then switch to a book whose impact decays and recover Obizhaeva and Wang's "
        "block-trickle-block schedule from the discrete optimum.")
TASKS = [
    "Give the kernel a power-law decay G(t) = (1 + t)^-0.4. What does the optimal schedule look like now?",
    "Add permanent impact (gamma > 0) in almgren_chriss. Does it change the schedule, or only the cost?",
    "Compare each schedule's cost with a square-root-law estimate, sigma sqrt(X / ADV).",
]


def run(seed=0):
    X, T, n, sigma, eta = 1.0, 1.0, 50, 0.3, 0.1
    lams = [0.0, 2.0, 10.0, 50.0, 250.0]
    plans = {lam: execution.almgren_chriss(X, T, n, sigma, eta, lam) for lam in lams}
    lab = labs.Lab()
    for lam, p in plans.items():
        half = p["t"][np.argmax(p["x"] <= 0.5 * X)]
        lab.row(f"risk aversion {lam:>5.0f}", f"half sold by t = {half:.2f}   expected cost {p['cost']:.4f}   "
                                              f"sd of cost {np.sqrt(p['var']):.4f}")
    twap = plans[0.0]
    assert np.allclose(np.diff(twap["x"]), -X / n) and abs(twap["cost"] - eta * X ** 2 / T) < 1e-9
    costs = [p["cost"] for p in plans.values()]
    variances = [p["var"] for p in plans.values()]
    assert np.all(np.diff(costs) > 0) and np.all(np.diff(variances) < 0)

    rho, m = 4.0, 200
    grid = np.arange(m + 1) * T / m
    v = execution.kernel_optimal(np.exp(-rho * grid), X)
    ow = execution.ow_closed_form(X, T, rho)
    cost = execution.kernel_cost(v, np.exp(-rho * grid))
    lab.row("Decaying impact: first and last block", f"{v[0]:.4f}, {v[-1]:.4f}   (closed form {ow['block']:.4f})")
    lab.row("Cost: optimum / closed form / all at once", f"{cost:.4f} / {ow['cost']:.4f} / {0.5 * X ** 2:.4f}")
    lab.note = ("With impact that depends on the trading rate, fear of risk means selling early. When the book refills, hit it "
                "at both ends and trickle in between, letting it recover.")
    assert abs(v[0] - ow["block"]) < 0.01 and abs(v[-1] - ow["block"]) < 0.01 and abs(cost - ow["cost"]) < 2e-3

    fig, ax = labs.figure(3, size=(12, 3.9))
    colors = [labs.CASH, labs.SPOT, labs.P, labs.IMPLIED, labs.LOSS]
    for (lam, p), c in zip(plans.items(), colors):
        ax[0].plot(p["t"], p["x"], color=c, label=f"lambda = {lam:g}")
    ax[0].set(title="Almgren-Chriss: shares still held", xlabel="time", ylabel="fraction of the order")
    ax[0].legend(fontsize=7.5)
    ax[1].plot(np.sqrt(variances), costs, "o-", color=labs.P)
    ax[1].set(title="The execution frontier", xlabel="sd of cost", ylabel="expected cost")
    ax[2].bar(grid, v, width=T / m, color=labs.SPOT)
    ax[2].set_yscale("log")
    ax[2].set(title="Decaying impact: block, trickle, block", xlabel="time", ylabel="shares traded (log)")
    lab.fig = fig
    return lab
