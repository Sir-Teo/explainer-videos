"""Lab 19: cross-validate a classifier on pure noise, with the features chosen outside and then inside the loop."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import learn

TITLE = "Leakage: selecting features before cross-validation"
GOAL = ("Give 60 cases 2,000 noise features and coin-flip labels, keep the 20 features most correlated with the labels, "
        "and estimate a 5-nearest-neighbour classifier's error by 5-fold cross-validation twice: with the selection "
        "done once on all the data, and with it redone inside every fold.")
TASKS = [
    "Lower p from 2,000 to 50 features. How much of the leak's optimism is left, and why?",
    "Give the first three features a real effect (add 0.8 * y to them). Do the two estimates now agree more closely?",
    "Replace the 5-nearest-neighbour vote by learn.logistic_ridge with lam = 1. Does the leak depend on the classifier?",
]


def top_features(X, y, keep):
    Xc, yc = X - X.mean(0), y - y.mean()
    c = np.abs(Xc.T @ yc) / np.sqrt((Xc ** 2).sum(0) * (yc ** 2).sum() + 1e-300)
    return np.argsort(-c)[:keep]


def cv_errors(X, y, keep, rng):
    """(error with selection before the loop, error with selection inside the loop) for one data set."""
    n = len(y)
    chosen = top_features(X, y, keep)  # the leak: the held-out labels helped to choose these
    wrong = right = 0
    for fold in learn.kfold(n, 5, rng):
        train = np.setdiff1d(np.arange(n), fold)
        wrong += np.sum(learn.knn_predict(X[train][:, chosen], y[train], X[fold][:, chosen], 5, classify=True) != y[fold])
        inside = top_features(X[train], y[train], keep)
        right += np.sum(learn.knn_predict(X[train][:, inside], y[train], X[fold][:, inside], 5, classify=True) != y[fold])
    return wrong / n, right / n


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, p, keep, reps = 60, 2000, 20, 60
    lab = labs.Lab()
    errs = np.array([cv_errors(rng.standard_normal((n, p)), (rng.random(n) < 0.5).astype(int), keep, rng)
                     for _ in range(reps)])
    wrong, right = errs.mean(0)
    se = errs.std(0, ddof=1) / np.sqrt(reps)
    lab.row("true error of any rule on coin-flip labels", "50.0%")
    lab.row("CV error, features selected before the loop", f"{wrong:.1%}   (± {se[0]:.1%})")
    lab.row("CV error, features selected inside the loop", f"{right:.1%}   (± {se[1]:.1%})")

    # how the leak grows with the number of features to choose from
    ps = [20, 50, 200, 500, 2000]
    curve = []
    for q in ps:
        e = np.array([cv_errors(rng.standard_normal((n, q)), (rng.random(n) < 0.5).astype(int), min(keep, q), rng)
                      for _ in range(20)])
        curve.append(e.mean(0))
    curve = np.array(curve)
    lab.row("leaky CV error at p = 20, 50, 200, 500, 2000", "  ".join(f"{v:.0%}" for v in curve[:, 0]))
    assert wrong < 0.25, "the leak makes noise look predictable"
    assert abs(right - 0.5) < 0.05, "honest cross-validation reports a coin flip"
    assert curve[-1, 0] < curve[0, 0] - 0.15, "the more features to choose from, the larger the leak"
    lab.note = ("Nothing here can be predicted, yet choosing the features with the held-out labels in view makes "
                "cross-validation report an error far below 50%; redoing the selection inside each fold reports the truth.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.linspace(0, 0.8, 33)
    ax[0].hist(errs[:, 0], bins=bins, color=labs.RED, alpha=0.7, label=f"selected before the loop: mean {wrong:.0%}")
    ax[0].hist(errs[:, 1], bins=bins, color=labs.GREEN, alpha=0.7, label=f"selected inside the loop: mean {right:.0%}")
    ax[0].axvline(0.5, color=labs.MUTED, ls="--", label="true error 50%")
    ax[0].set(title=f"CV error on {reps} pure-noise data sets (n = 60, p = 2,000)", xlabel="5-fold CV error",
              ylabel="data sets")
    ax[0].legend(loc="upper left")
    ax[1].plot(ps, curve[:, 0], "o-", color=labs.RED, label="selected before the loop")
    ax[1].plot(ps, curve[:, 1], "o-", color=labs.GREEN, label="selected inside the loop")
    ax[1].axhline(0.5, color=labs.MUTED, ls="--")
    ax[1].set(xscale="log", ylim=(0, 0.7), title="The leak grows with the number of candidate features",
              xlabel="noise features p (20 kept)", ylabel="mean CV error")
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab
