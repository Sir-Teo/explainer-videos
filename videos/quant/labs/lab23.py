"""Lab 23: the frontier, the tangency portfolio, and what ten years of data do to both."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import premia

TITLE = "The efficient frontier, true and estimated"
GOAL = ("Build a market where the CAPM holds exactly, draw its frontier and tangency portfolio, then re-estimate "
        "everything from ten years of simulated returns and measure how much Sharpe ratio the estimate throws away.")
TASKS = [
    "Raise the sample from 120 to 1,200 months. How fast does the estimated tangency portfolio recover?",
    "Regress simulated returns on the market with premia.capm_betas; do the alphas reject the CAPM at 5%?",
    "Replace the estimated means by one common number. Which portfolio do you get, and how does it do?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, rf = 8, 0.0
    beta = np.linspace(0.5, 1.6, n)
    resid = np.linspace(0.20, 0.12, n) / np.sqrt(12)
    mkt_mu, mkt_sd = 0.06 / 12, 0.16 / np.sqrt(12)
    Sigma = np.outer(beta, beta) * mkt_sd ** 2 + np.diag(resid ** 2)
    # expected returns that make one portfolio (the "market") the tangency portfolio: mu = beta_m * premium
    w_m = np.full(n, 1 / n)
    mu = Sigma @ w_m / (w_m @ Sigma @ w_m) * mkt_mu
    true = premia.tangency(mu, Sigma, rf)
    sr_true = np.sqrt(12) * true["mean"] / true["sd"]
    lost, claimed = [], []
    for _ in range(400):
        R = rng.multivariate_normal(mu, Sigma, 120)
        est = premia.tangency(R.mean(0), np.cov(R.T), rf)
        claimed.append(np.sqrt(12) * abs(est["mean"]) / est["sd"])  # what the optimizer believes it has found
        lost.append(np.sqrt(12) * (est["w"] @ mu) / np.sqrt(est["w"] @ Sigma @ est["w"]))
    lost, claimed = np.array(lost), np.array(claimed)
    lab = labs.Lab()
    lab.row("True tangency portfolio", f"Sharpe {sr_true:.2f}; weights all {true['w'][0]:.3f} (it is the equal-weight market)")
    lab.row("Estimated from 10 years, true Sharpe", f"median {np.median(lost):.2f}, 5%-95% {np.percentile(lost, 5):.2f} to "
                                                    f"{np.percentile(lost, 95):.2f}")
    lab.row("Sharpe the optimizer reports in sample", f"median {np.median(claimed):.2f}")
    lab.note = ("The optimizer is an error maximizer: it loads on whatever looked best in sample. Parts 30 and 31 "
                "are about taming it.")
    assert np.allclose(true["w"], w_m, atol=1e-6) and np.median(lost) < 0.75 * sr_true < np.median(claimed)

    fig, ax = labs.figure(2, size=(11, 4.2))
    m = np.linspace(0.001, 0.012, 200)
    sd = premia.frontier_sigma(m, mu, Sigma)
    ax[0].plot(100 * np.sqrt(12) * sd, 1200 * m, color=labs.P, label="true frontier")
    R = rng.multivariate_normal(mu, Sigma, 120)
    mu_hat, S_hat = R.mean(0), np.cov(R.T)
    m2 = np.linspace(mu_hat.min(), mu_hat.max() * 1.3, 200)
    ax[0].plot(100 * np.sqrt(12) * premia.frontier_sigma(m2, mu_hat, S_hat), 1200 * m2, color=labs.LOSS, ls="--",
               label="estimated from one 10-year sample")
    ax[0].scatter(100 * np.sqrt(12 * np.diag(Sigma)), 1200 * mu, color=labs.SPOT, s=18, zorder=3, label="the assets")
    ax[0].plot(100 * np.sqrt(12) * true["sd"], 1200 * true["mean"], "*", color=labs.P, ms=12)
    ax[0].set(title="Mean against volatility (annual, %)", xlabel="volatility", ylabel="expected excess return",
              xlim=(8, 34), ylim=(0, 14))
    ax[0].legend(fontsize=8)
    ax[1].hist(lost, bins=40, color=labs.SPOT)
    ax[1].axvline(sr_true, color=labs.P, ls="--", label=f"true maximum {sr_true:.2f}")
    ax[1].set(title="True Sharpe ratio of the estimated tangency portfolio", xlabel="annual Sharpe ratio")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
