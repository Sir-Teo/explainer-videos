"""Lab 28: screen fifty columns of noise as Freedman did, and measure the optimism 2 sigma^2 d / n of a polynomial fit."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import select

TITLE = "Freedman's paradox and the price of a parameter"
GOAL = ("Repeat Freedman's two-round regression on pure noise 300 times with statkit.select, then fit polynomials of "
        "degree 0 to 10 to 30 noisy points 600 times and compare the gap between new-response and training error "
        "with 2 sigma^2 d / n for d = degree + 1 coefficients. Count how often AIC and BIC choose each degree.")
TASKS = [
    "Screen at alpha = 0.05 instead of 0.25 (select.freedman's last argument). Is round two significant more or less often?",
    "Raise n from 30 to 300 in the polynomial experiment. Which criterion's choice of degree settles down, and which keeps overfitting?",
    "Replace AIC by select.aicc in the tally. How much of AIC's overfitting at n = 30 does the correction remove?",
]


def truth(x):
    return np.sin(2.5 * x) + 0.5 * x


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Freedman (1983): 100 observations, 50 predictors, all noise; keep those with p < 0.25 and refit.
    reps = 300
    runs = [select.freedman(100, 50, rng) for _ in range(reps)]
    p1 = np.array([r["first"]["pF"] for r in runs])
    p2 = np.array([r["second"]["pF"] for r in runs])
    kept = np.array([len(r["second"]["cols"]) for r in runs])
    lab.row("round 1 (all 50 columns): overall F significant at 5%", f"{np.mean(p1 < 0.05):.1%}   (honest: 5%)")
    lab.row("round 2 (the screened columns): significant at 5%", f"{np.mean(p2 < 0.05):.1%}   (film: 94.7% of 1,000)")
    lab.row("columns kept by the screen, median", f"{np.median(kept):.0f}   (50 x 0.25 = 12.5 expected)")
    assert np.mean(p1 < 0.05) < 0.11, "the first-round F test is honest"
    assert np.mean(p2 < 0.05) > 0.85, "after screening, noise looks significant"
    assert 10 <= np.median(kept) <= 15

    # 2. Optimism: thirty points from a smooth curve, noise sd 0.5, polynomials of degree 0..10.
    n, sigma, R = 30, 0.5, 600
    x = np.linspace(-1.5, 1.5, n)
    degs = np.arange(11)
    H = [select.hat_matrix(np.polynomial.legendre.legvander(x / 1.5, d)) for d in degs]
    train, new = np.zeros(len(degs)), np.zeros(len(degs))
    picks = {"AIC": np.zeros(len(degs)), "BIC": np.zeros(len(degs))}
    for _ in range(R):
        y = truth(x) + sigma * rng.standard_normal(n)
        y2 = truth(x) + sigma * rng.standard_normal(n)  # new responses at the same x
        crit = {"AIC": [], "BIC": []}
        for k, d in enumerate(degs):
            fit = H[k] @ y
            rss = float(np.sum((y - fit) ** 2))
            train[k] += rss / n / R
            new[k] += np.mean((y2 - fit) ** 2) / R
            ll = select.gaussian_ll(rss, n)
            crit["AIC"].append(select.aic(ll, d + 2))
            crit["BIC"].append(select.bic(ll, d + 2, n))
        for name in picks:
            picks[name][int(np.argmin(crit[name]))] += 1 / R
    gap, theory = new - train, 2 * sigma ** 2 * (degs + 1) / n
    for d in (1, 3, 10):
        lab.row(f"degree {d}: new-response error minus training error", f"{gap[d]:.3f}   (2 sigma^2 (degree + 1) / n = {theory[d]:.3f})")
    best = int(np.argmin(new))
    lab.row("degree with the lowest new-response error", f"{best}   (training error is lowest at degree {int(np.argmin(train))})")
    mean_deg = {k: float(v @ degs) for k, v in picks.items()}
    lab.row("mean degree chosen: AIC, BIC", f"{mean_deg['AIC']:.2f}, {mean_deg['BIC']:.2f}")
    assert np.max(np.abs(gap - theory)) < 0.03, "the optimism of least squares is 2 sigma^2 d / n"
    assert np.argmin(train) == 10 and 3 <= best <= 6, "training error always prefers the largest model"
    assert mean_deg["BIC"] < mean_deg["AIC"], "BIC's log n per parameter chooses smaller models than AIC's 2"

    # 3. The leave-one-out shortcut against refitting thirty times.
    X = np.polynomial.legendre.legvander(x / 1.5, 3)
    y = truth(x) + sigma * rng.standard_normal(n)
    brute = np.mean([(y[i] - X[i] @ np.linalg.lstsq(np.delete(X, i, 0), np.delete(y, i), rcond=None)[0]) ** 2 for i in range(n)])
    lab.row("leave-one-out error, degree 3: shortcut, refitting", f"{select.press(X, y):.5f}, {brute:.5f}")
    assert abs(select.press(X, y) - brute) < 1e-9, "PRESS is residual / (1 - h_ii), exactly"
    lab.note = ("Selection on the same data manufactures significance, and each fitted coefficient buys 2 sigma^2 / n "
                "of optimism: training error keeps falling while the error on new responses turns up.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.linspace(0, 1, 21)
    ax[0].hist(p1, bins=bins, color=labs.BLUE, alpha=0.6, label="round 1: all 50 noise columns")
    ax[0].hist(p2, bins=bins, color=labs.RED, alpha=0.6, label="round 2: the columns that passed")
    ax[0].axhline(reps / 20, color=labs.MUTED, ls="--", label="honest p-values")
    ax[0].set(title="Freedman's paradox: overall F-test p-values", xlabel="p-value", ylabel=f"count of {reps} repeats")
    ax[0].legend()
    ax[1].plot(degs, train, "o-", color=labs.BLUE, label="training error")
    ax[1].plot(degs, new, "o-", color=labs.RED, label="error on new responses")
    ax[1].plot(degs, train + theory, "--", color=labs.GOLD, label="training error + 2 sigma^2 (degree + 1) / n")
    ax[1].axhline(sigma ** 2, color=labs.MUTED, ls=":", label="noise variance")
    ax[1].set(title="Optimism: thirty points, 600 data sets", xlabel="polynomial degree (0 to 2 are off the scale)", ylabel="mean squared error",
              ylim=(0, 0.6))
    ax[1].legend()
    lab.fig = fig
    return lab
