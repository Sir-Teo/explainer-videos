"""statkit.learn: prediction for Part 19 of *Statistics, Built* ("Learning from Data").

k-nearest neighbours, K-fold cross-validation with the one-standard-error rule, naive Bayes for word counts
(multinomial and Poisson, as Mosteller & Wallace), ridge-penalized logistic regression, CART trees with cost-complexity
pruning, ridge and the lasso (coordinate descent, with its path), and classification metrics.  Checked in
``tests/test_stats_kit_learn.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


# ---------------------------------------------------------------------------------------------------------------------
# Cross-validation
# ---------------------------------------------------------------------------------------------------------------------
def kfold(n: int, k: int, rng: np.random.Generator) -> list[np.ndarray]:
    return np.array_split(rng.permutation(n), k)


def cv_score(fit_predict, X, y, k: int, rng: np.random.Generator, loss=None) -> dict:
    """K-fold CV of ``fit_predict(Xtr, ytr, Xte) -> predictions``; returns the mean loss, its SE across folds and
    the per-fold losses (squared error by default)."""
    X, y = np.asarray(X), np.asarray(y)
    loss = loss or (lambda yt, yp: float(np.mean((yt - yp) ** 2)))
    folds = kfold(len(y), k, rng)
    per = []
    for f in folds:
        tr = np.setdiff1d(np.arange(len(y)), f)
        per.append(loss(y[f], fit_predict(X[tr], y[tr], X[f])))
    per = np.asarray(per)
    return {"mean": float(per.mean()), "se": float(per.std(ddof=1) / np.sqrt(k)), "folds": per}


def one_se_rule(means, ses) -> tuple[int, int]:
    """Breiman et al. (1984): the index of the minimum, and of the simplest model (smallest index; order the models
    from simplest to most complex) whose CV error is within one SE of the minimum."""
    means, ses = np.asarray(means), np.asarray(ses)
    best = int(np.argmin(means))
    ok = np.flatnonzero(means <= means[best] + ses[best])
    return best, int(ok.min())


# ---------------------------------------------------------------------------------------------------------------------
# k-nearest neighbours
# ---------------------------------------------------------------------------------------------------------------------
def knn_predict(Xtr, ytr, Xte, k: int, classify: bool = False) -> np.ndarray:
    Xtr, Xte = np.atleast_2d(np.asarray(Xtr, float)), np.atleast_2d(np.asarray(Xte, float))
    if Xtr.shape[0] == 1 and Xtr.shape[1] != 1:
        Xtr, Xte = Xtr.T, Xte.T
    ytr = np.asarray(ytr)
    d = ((Xte[:, None, :] - Xtr[None, :, :]) ** 2).sum(-1)
    nn = np.argsort(d, axis=1, kind="stable")[:, :k]
    vals = ytr[nn]
    if classify:
        return (vals.mean(1) > 0.5).astype(int)
    return vals.mean(1)


# ---------------------------------------------------------------------------------------------------------------------
# Naive Bayes for word counts
# ---------------------------------------------------------------------------------------------------------------------
@dataclass
class PoissonNB:
    """Mosteller & Wallace's model in its simplest form: each word count ~ Poisson(rate_c x length), independently,
    with class rates estimated (with a small pseudo-count) from the training papers."""
    rates: np.ndarray = field(default_factory=lambda: np.zeros(0))
    log_prior: np.ndarray = field(default_factory=lambda: np.zeros(0))

    def fit(self, counts, lengths, labels, alpha: float = 0.5):
        counts, lengths, labels = np.asarray(counts, float), np.asarray(lengths, float), np.asarray(labels, int)
        self.rates = np.array([(counts[labels == c].sum(0) + alpha) / lengths[labels == c].sum() for c in (0, 1)])
        self.log_prior = np.log(np.array([np.mean(labels == 0), np.mean(labels == 1)]))
        return self

    def log_odds(self, counts, lengths, prior: bool = False) -> np.ndarray:
        """log P(class 1 | x) / P(class 0 | x): sum_w x_w log(r1/r0) - t sum_w (r1 - r0) [+ the prior log odds]."""
        counts, lengths = np.atleast_2d(np.asarray(counts, float)), np.asarray(lengths, float).ravel()
        lr = counts @ np.log(self.rates[1] / self.rates[0]) - lengths * (self.rates[1] - self.rates[0]).sum()
        return lr + (self.log_prior[1] - self.log_prior[0] if prior else 0.0)

    def contributions(self, counts, lengths) -> np.ndarray:
        """Each word's term in the log odds for one document."""
        counts = np.asarray(counts, float)
        return counts * np.log(self.rates[1] / self.rates[0]) - float(lengths) * (self.rates[1] - self.rates[0])


def logistic_ridge(X, y, lam: float = 0.0, max_iter: int = 100, tol: float = 1e-10) -> np.ndarray:
    """Logistic regression with an intercept and a ridge penalty lam * |beta|^2 / 2 on the slopes, by Newton's method.
    Returns (intercept, slopes...)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    Z = np.column_stack([np.ones(len(y)), X])
    b = np.zeros(Z.shape[1])
    P = lam * np.eye(Z.shape[1])
    P[0, 0] = 0.0
    for _ in range(max_iter):
        p = 1 / (1 + np.exp(-(Z @ b)))
        g = Z.T @ (y - p) - P @ b
        H = Z.T @ (Z * (p * (1 - p))[:, None]) + P
        step = np.linalg.solve(H, g)
        b += step
        if np.max(np.abs(step)) < tol:
            break
    return b


def logistic_predict(b, X) -> np.ndarray:
    return 1 / (1 + np.exp(-(b[0] + np.asarray(X, float) @ b[1:])))


# ---------------------------------------------------------------------------------------------------------------------
# Trees (CART)
# ---------------------------------------------------------------------------------------------------------------------
@dataclass
class Node:
    value: float
    n: int
    sse: float
    feature: int = -1
    threshold: float = 0.0
    left: "Node | None" = None
    right: "Node | None" = None

    @property
    def leaf(self) -> bool:
        return self.left is None


def _impurity(y, classify):
    if classify:
        p = y.mean()
        return len(y) * 2 * p * (1 - p)  # n times the Gini index
    return float(np.sum((y - y.mean()) ** 2))


def grow_tree(X, y, max_depth: int = 6, min_leaf: int = 5, classify: bool = False, depth: int = 0) -> Node:
    """Breiman, Friedman, Olshen & Stone (1984): greedy binary splits minimizing squared error (or Gini)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    node = Node(float(y.mean()), len(y), _impurity(y, classify))
    if depth >= max_depth or len(y) < 2 * min_leaf or node.sse <= 1e-12:
        return node
    best = (node.sse, -1, 0.0)
    for j in range(X.shape[1]):
        order = np.argsort(X[:, j], kind="stable")
        xs, ys = X[order, j], y[order]
        for i in range(min_leaf, len(y) - min_leaf + 1):
            if xs[i - 1] == xs[i]:
                continue
            s = _impurity(ys[:i], classify) + _impurity(ys[i:], classify)
            if s < best[0] - 1e-12:
                best = (s, j, (xs[i - 1] + xs[i]) / 2)
    if best[1] < 0:
        return node
    j, t = best[1], best[2]
    m = X[:, j] <= t
    node.feature, node.threshold = j, t
    node.left = grow_tree(X[m], y[m], max_depth, min_leaf, classify, depth + 1)
    node.right = grow_tree(X[~m], y[~m], max_depth, min_leaf, classify, depth + 1)
    return node


def tree_predict(node: Node, X) -> np.ndarray:
    X = np.atleast_2d(np.asarray(X, float))
    out = np.empty(len(X))
    for i, x in enumerate(X):
        n = node
        while not n.leaf:
            n = n.left if x[n.feature] <= n.threshold else n.right
        out[i] = n.value
    return out


def leaves(node: Node) -> list[Node]:
    return [node] if node.leaf else leaves(node.left) + leaves(node.right)


def _subtree_cost(node: Node) -> float:
    return sum(l.sse for l in leaves(node))


def prune_path(root: Node) -> list[tuple[float, int]]:
    """Weakest-link (cost-complexity) pruning: repeatedly collapse the internal node with the smallest increase in
    error per leaf removed.  Returns (alpha, number of leaves) along the path; prunes ``root`` in place to one leaf."""
    path = [(0.0, len(leaves(root)))]
    while not root.leaf:
        best, bn = np.inf, None
        stack = [root]
        while stack:
            n = stack.pop()
            if n.leaf:
                continue
            g = (n.sse - _subtree_cost(n)) / (len(leaves(n)) - 1)
            if g < best:
                best, bn = g, n
            stack += [n.left, n.right]
        bn.left = bn.right = None
        bn.feature = -1
        path.append((float(best), len(leaves(root))))
    return path


def prune_to(root: Node, n_leaves: int) -> Node:
    """A copy of ``root`` pruned by weakest links until it has at most ``n_leaves`` leaves."""
    import copy

    t = copy.deepcopy(root)
    while len(leaves(t)) > n_leaves:
        best, bn = np.inf, None
        stack = [t]
        while stack:
            n = stack.pop()
            if n.leaf:
                continue
            g = (n.sse - _subtree_cost(n)) / (len(leaves(n)) - 1)
            if g < best:
                best, bn = g, n
            stack += [n.left, n.right]
        bn.left = bn.right = None
        bn.feature = -1
    return t


# ---------------------------------------------------------------------------------------------------------------------
# Ridge and the lasso
# ---------------------------------------------------------------------------------------------------------------------
def standardize(X):
    X = np.asarray(X, float)
    mu, sd = X.mean(0), X.std(0)
    sd = np.where(sd > 0, sd, 1.0)
    return (X - mu) / sd, mu, sd


def ridge(X, y, lam: float) -> np.ndarray:
    """Ridge on centred y and standardized X: (X'X + lam I)^{-1} X'y (no intercept; centre first)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    return np.linalg.solve(X.T @ X + lam * np.eye(X.shape[1]), X.T @ y)


def soft(z, t):
    return np.sign(z) * np.maximum(np.abs(z) - t, 0.0)


def lasso(X, y, lam: float, b0=None, max_iter: int = 10_000, tol: float = 1e-10) -> np.ndarray:
    """Tibshirani (1996), by cyclic coordinate descent: minimize |y - Xb|^2 / (2n) + lam |b|_1 (centred y, X)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    b = np.zeros(p) if b0 is None else np.asarray(b0, float).copy()
    r = y - X @ b
    cs = (X ** 2).sum(0) / n
    for _ in range(max_iter):
        delta = 0.0
        for j in range(p):
            old = b[j]
            zj = X[:, j] @ r / n + cs[j] * old
            b[j] = soft(zj, lam) / cs[j]
            if b[j] != old:
                r -= X[:, j] * (b[j] - old)
                delta = max(delta, abs(b[j] - old))
        if delta < tol:
            break
    return b


def lasso_path(X, y, lams) -> np.ndarray:
    """Coefficients along a decreasing sequence of lambdas, warm-started."""
    out, b = [], None
    for lam in lams:
        b = lasso(X, y, lam, b0=b)
        out.append(b.copy())
    return np.array(out)


# ---------------------------------------------------------------------------------------------------------------------
# Classification metrics
# ---------------------------------------------------------------------------------------------------------------------
def confusion(y, yhat) -> dict:
    y, yhat = np.asarray(y, int), np.asarray(yhat, int)
    tp = int(np.sum((y == 1) & (yhat == 1)))
    tn = int(np.sum((y == 0) & (yhat == 0)))
    fp = int(np.sum((y == 0) & (yhat == 1)))
    fn = int(np.sum((y == 1) & (yhat == 0)))
    prec = tp / (tp + fp) if tp + fp else float("nan")
    rec = tp / (tp + fn) if tp + fn else float("nan")
    return {"tp": tp, "tn": tn, "fp": fp, "fn": fn, "accuracy": (tp + tn) / len(y), "precision": prec, "recall": rec,
            "specificity": tn / (tn + fp) if tn + fp else float("nan"),
            "f1": 2 * prec * rec / (prec + rec) if prec + rec else float("nan")}


def pr_curve(scores, labels) -> tuple[np.ndarray, np.ndarray]:
    """Precision and recall at every threshold, highest score first."""
    s, y = np.asarray(scores, float), np.asarray(labels, int)
    o = np.argsort(-s, kind="stable")
    tp = np.cumsum(y[o])
    k = np.arange(1, len(y) + 1)
    return tp / k, tp / max(1, y.sum())


def auc(scores, labels) -> float:
    """P(score of a random positive > score of a random negative) + half the ties (Part 16's Mann-Whitney)."""
    s, y = np.asarray(scores, float), np.asarray(labels, int)
    pos, neg = s[y == 1], s[y == 0]
    gt = (pos[:, None] > neg[None, :]).sum() + 0.5 * (pos[:, None] == neg[None, :]).sum()
    return float(gt / (len(pos) * len(neg)))
