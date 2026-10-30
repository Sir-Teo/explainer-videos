"""Precompute everything numerical in Part 6 of the AI series ("Classical ML").

    python -m videos.ai.ai6.compute              # everything missing (Part 1's books are reused: .cache/ai1)
    python -m videos.ai.ai6.compute --force svm

Results are cached in ``.cache/ai6/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Every method is written
out here in numpy (no machine-learning library), and every number the narration quotes is computed here.  Every
random choice is seeded; the whole module runs in about ten CPU-minutes on one core.

The task, for every method: who wrote this page, Jane Austen or Charles Dickens?  Pages are 1,000-word chunks of
five novels (Pride and Prejudice and Emma; A Tale of Two Cities, Great Expectations and A Christmas Carol); a page
is described by how often it uses the 70 commonest words (per 1,000 words), as Mosteller and Wallace described the
Federalist papers in 1964.  70% of the pages train, 30% are held out to test.  The pictures use two of the 70
numbers: how often a page says "the", and how often it says "not".

Other parts read ``load("pages")``, ``split()`` and ``standardize()`` (Parts 7, 8 and 11): keep them as they are.

Items:
    pages        the pages, their 70 rates, labels, the train/test split, the two plotted rates, one test page's text
    zipf         least squares on Zipf's law
    gaussmarkov  Gauss-Markov by simulation: least squares against other unbiased estimators of a slope
    lsq          least squares on the pages: normal equations, QR and the pseudoinverse; a duplicated column
    ridge        ridge regression through the SVD: the shrinkage factor of every direction, cross-validated
    lasso        the lasso path by coordinate descent (KKT checked), cross-validated; the elastic net
    logistic     logistic regression on the two rates (gradient descent, the probability sheet) and on all 70
    irls         Newton's method (IRLS) against gradient descent; what happens without a penalty
    calibration  reliability of cross-validated probabilities: logistic regression, naive Bayes, Platt scaling
    nbvslr       naive Bayes against logistic regression as the training set grows (Ng & Jordan, 2002)
    lda          Fisher's discriminant: the separation along every direction, the generalized eigenproblem
    knn          k nearest neighbours: regions for many k, accuracy, cross-validation
    coverhart    1-NN on two Gaussians with a known Bayes error, against the Cover-Hart bound
    curse        the curse of dimensionality, measured: distances in a cube; neighbours among noisy words
    kernel       the kernel lift, Mercer (Gram eigenvalues), the RBF's features, the representer theorem
    svm          SMO for the soft-margin dual: the margin, support vectors, KKT, decision regions over C and gamma
    trees        a decision tree on the two rates (depth 1 to 6), impurity scans, cross-validated depth
    bagging      the variance of an average of correlated trees, rho*s2 + (1 - rho)*s2/B, measured; random forests
    adaboost     AdaBoost with stumps: the exponential loss falling, alpha by line search, the weights
    xgb          gradient boosting with second-order (XGBoost) splits; the gain formula checked
    metrics      ROC and precision-recall curves, AUC as a ranking probability, cross-validation's spread
    board        every method on the same ten cross-validation folds, with 2 rates and with 70
"""

from __future__ import annotations

import collections
import math
import re

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai6")
load = CACHE.load

AUSTEN = {1342: "Pride and Prejudice", 158: "Emma"}
DICKENS = {98: "A Tale of Two Cities", 1400: "Great Expectations", 46: "A Christmas Carol"}
PAGE = 1000  # words per page
N_WORDS = 70
PLOT = ("the", "not")  # the two rates in every picture
GRID = 120  # resolution of the decision-region pictures
FOLDS = 10


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def book_words(n: int) -> list[str]:
    from videos.ai.ai1 import compute as c1

    t = c1.strip_gutenberg((c1.BOOK_DIR / f"{n}.txt").read_text(encoding="utf-8", errors="replace"))
    t = t.translate(c1.QUOTES).lower()
    return re.findall(r"[a-z]+(?:'[a-z]+)?", t)


# ---------------------------------------------------------------------------
def compute_pages():
    books = {n: book_words(n) for n in [*AUSTEN, *DICKENS]}
    allw = collections.Counter(w for ws in books.values() for w in ws)
    vocab = [w for w, _ in allw.most_common(N_WORDS)]
    X, y, book, text = [], [], [], []
    for n, ws in books.items():
        for i in range(0, len(ws) - PAGE + 1, PAGE):
            ch = ws[i:i + PAGE]
            c = collections.Counter(ch)
            X.append([1000 * c[w] / PAGE for w in vocab])
            y.append(0 if n in AUSTEN else 1)
            book.append(n)
            text.append(" ".join(ch[:60]))
    X, y, book = np.array(X), np.array(y), np.array(book)
    g = rng(1964)  # Mosteller & Wallace, 1964
    test = np.zeros(len(y), bool)
    for lab in (0, 1):  # 30% of each author's pages held out
        idx = np.nonzero(y == lab)[0]
        test[g.choice(idx, size=int(round(0.3 * len(idx))), replace=False)] = True
    j = [vocab.index(w) for w in PLOT]
    ex = int(np.nonzero(test & (book == 1400))[0][3])
    assert set(PLOT) <= set(vocab) and 600 < len(y) < 700
    return dict(vocab=vocab, X=X, y=y, book=book, test=test, plot=list(PLOT), X2=X[:, j], example=text[ex],
                example_label=int(y[ex]), example_i=ex, n_pages=len(y), n_austen=int((y == 0).sum()),
                n_dickens=int((y == 1).sum()), titles={**AUSTEN, **DICKENS})


def split():
    p = load("pages")
    X, y, test = np.asarray(p["X"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
    return X, y, test, np.asarray(p["X2"])


def standardize(Xtr, *others):
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
    return [(Xtr - mu) / sd] + [(o - mu) / sd for o in others] + [mu, sd]


def grid2(X2):
    """A grid over the two plotted rates, a little beyond the data."""
    lo, hi = X2.min(0), X2.max(0)
    pad = 0.06 * (hi - lo)
    xs = np.linspace(lo[0] - pad[0], hi[0] + pad[0], GRID)
    ys = np.linspace(lo[1] - pad[1], hi[1] + pad[1], GRID)
    G = np.stack(np.meshgrid(xs, ys), -1).reshape(-1, 2)
    return xs, ys, G


def kfold(y, k=FOLDS, seed=10):
    """Stratified folds: each author's pages dealt round-robin after a seeded shuffle.  Returns a fold index per
    page."""
    g = rng(seed)
    f = np.empty(len(y), int)
    for lab in (0, 1):
        idx = np.nonzero(y == lab)[0]
        idx = idx[g.permutation(len(idx))]
        f[idx] = np.arange(len(idx)) % k
    return f


def acc_of(score, y, thr=0.5):
    return float(((np.asarray(score) > thr) == np.asarray(y)).mean())


# ---------------------------------------------------------------------------
def compute_zipf():
    from videos.ai.ai1 import compute as c1

    words = re.findall(r"[a-z]+(?:'[a-z]+)?", c1.text("train").lower())
    cnt = collections.Counter(words).most_common(1000)
    f = np.array([c for _, c in cnt], float)
    r = np.arange(1, len(f) + 1, dtype=float)
    A = np.stack([np.ones_like(r), np.log10(r)], 1)
    b = np.log10(f)
    beta = np.linalg.solve(A.T @ A, A.T @ b)  # the normal equations
    res = b - A @ beta
    r2 = 1 - (res ** 2).sum() / ((b - b.mean()) ** 2).sum()
    assert np.allclose(beta, np.linalg.lstsq(A, b, rcond=None)[0]) and -1.25 < beta[1] < -0.8
    return dict(words=[w for w, _ in cnt[:12]], f=f, r=r, beta=beta, r2=float(r2), n_words=len(words))


# ---------------------------------------------------------------------------
GM_X = np.linspace(1.0, 10.0, 12)  # the design: twelve evenly spaced x
GM_BETA = (1.0, 0.5)


def theil_sen(Y, x):
    i, j = np.triu_indices(len(x), 1)
    return np.median((Y[:, j] - Y[:, i]) / (x[j] - x[i]), axis=1)


def compute_gaussmarkov():
    """Many datasets y = 1 + 0.5 x + noise on the same twelve x; four estimators of the slope on each."""
    x = GM_X
    n, R = len(x), 40000
    A = np.stack([np.ones(n), x], 1)
    C_ols = np.linalg.solve(A.T @ A, A.T)  # the least-squares weights: slope = C_ols[1] @ y
    c_end = np.zeros(n)
    c_end[0], c_end[-1] = -1 / (x[-1] - x[0]), 1 / (x[-1] - x[0])  # the slope through the two end points
    # another unbiased linear estimator: OLS plus d with d . 1 = d . x = 0 (so it adds nothing on average)
    P = A @ C_ols
    d = (np.eye(n) - P) @ np.cos(np.arange(n) * 1.3)
    d *= 0.12 / np.linalg.norm(d)
    c_mix = C_ols[1] + d
    assert abs(c_mix @ np.ones(n)) < 1e-12 and abs(c_mix @ x - 1) < 1e-12 and abs(c_end @ x - 1) < 1e-12
    out = dict(x=x, beta=list(GM_BETA), R=R, w_ols=C_ols[1], w_end=c_end, w_mix=c_mix)
    theory = {"ols": float(C_ols[1] @ C_ols[1]), "end": float(c_end @ c_end), "mix": float(c_mix @ c_mix)}
    out["theory"] = theory
    for noise, seed in (("gauss", 1809), ("t3", 1821)):
        g = rng(seed)
        if noise == "gauss":
            E = g.standard_normal((R, n))
        else:  # Student's t with 3 degrees of freedom, scaled to variance 1: heavy tails, same variance
            E = g.standard_t(3, (R, n)) / math.sqrt(3.0)
        Y = GM_BETA[0] + GM_BETA[1] * x + E
        est = {"ols": Y @ C_ols[1], "end": Y @ c_end, "mix": Y @ c_mix, "ts": theil_sen(Y, x)}
        out[noise] = {k: dict(mean=float(v.mean()), var=float(v.var()), se_mean=float(v.std() / math.sqrt(R)))
                      for k, v in est.items()}
        if noise == "gauss":
            bins = np.linspace(0.5 - 0.42, 0.5 + 0.42, 43)
            out["hist_bins"] = bins
            for k in ("ols", "end", "ts"):
                out[f"hist_{k}"] = np.histogram(est[k], bins=bins)[0].astype(float)
            out["samples"] = Y[:6]
    return out


# ---------------------------------------------------------------------------
def compute_lsq():
    """Least squares on the pages (a 0/1 target): three ways to solve it, and what a duplicated column does."""
    X, y, test, _ = split()
    p = load("pages")
    Ztr, Zte, _, _ = standardize(X[~test], X[test])
    ytr = y[~test].astype(float)
    A = np.hstack([np.ones((len(Ztr), 1)), Ztr])
    b_ne = np.linalg.solve(A.T @ A, A.T @ ytr)
    Q, Rm = np.linalg.qr(A)
    b_qr = np.linalg.solve(Rm, Q.T @ ytr)
    b_pi = np.linalg.pinv(A) @ ytr
    s = np.linalg.svd(A, compute_uv=False)
    out = dict(kappa_A=float(s[0] / s[-1]), kappa_AtA=float((s[0] / s[-1]) ** 2),
               diff_ne_qr=float(np.abs(b_ne - b_qr).max()), diff_qr_pinv=float(np.abs(b_qr - b_pi).max()),
               acc_train=acc_of(A @ b_qr, ytr), acc_test=acc_of(np.hstack([np.ones((len(Zte), 1)), Zte]) @ b_qr, y[test]))
    # a duplicated column: "not" twice.  A^T A is singular; the pseudoinverse picks the shortest weights.
    j = p["vocab"].index("not")
    A2 = np.hstack([A, A[:, [1 + j]]])
    s2 = np.linalg.svd(A2, compute_uv=False)
    b2 = np.linalg.pinv(A2) @ ytr
    out.update(rank_dup=int(np.linalg.matrix_rank(A2)), cols_dup=int(A2.shape[1]), smin_dup=float(s2[-1] / s2[0]),
               w_not=float(b_qr[1 + j]), w_not_a=float(b2[1 + j]), w_not_b=float(b2[-1]),
               same_fit=float(np.abs(A2 @ b2 - A @ b_qr).max()))
    try:
        b3 = np.linalg.solve(A2.T @ A2, A2.T @ ytr)
        out["ne_dup"] = "solved"
        out["ne_dup_norm"] = float(np.linalg.norm(b3))
        out["ne_dup_resid"] = float(np.abs(A2 @ b3 - A @ b_qr).max())
    except np.linalg.LinAlgError:
        out["ne_dup"] = "singular"
    assert out["diff_qr_pinv"] < 1e-8 and abs(out["w_not_a"] - out["w_not_b"]) < 1e-8
    assert abs(out["w_not_a"] + out["w_not_b"] - out["w_not"]) < 1e-8
    return out


# ---------------------------------------------------------------------------
def ridge_svd(Z, yc, lam):
    U, d, Vt = np.linalg.svd(Z, full_matrices=False)
    return Vt.T @ ((d / (d ** 2 + lam)) * (U.T @ yc))


def compute_ridge():
    """Ridge regression on the 70 standardized rates (target 0/1, centred), through the SVD."""
    X, y, test, _ = split()
    Ztr, Zte, _, _ = standardize(X[~test], X[test])
    ytr = y[~test].astype(float)
    yc = ytr - ytr.mean()
    U, d, Vt = np.linalg.svd(Ztr, full_matrices=False)
    lams = np.logspace(-1, 5, 49)
    w_chk = ridge_svd(Ztr, yc, 30.0)
    assert np.allclose(w_chk, np.linalg.solve(Ztr.T @ Ztr + 30.0 * np.eye(Ztr.shape[1]), Ztr.T @ yc))
    shows = [1.0, 30.0, 1000.0]
    shrink = {str(l_): (d ** 2 / (d ** 2 + l_)) for l_ in shows}
    df = np.array([float((d ** 2 / (d ** 2 + l_)).sum()) for l_ in lams])
    uy = U.T @ yc  # how much of the target lies along each direction
    # ten-fold cross-validation on the training pages: squared error and accuracy at every lambda
    f = kfold(ytr, seed=1970)
    mse, acc = np.zeros((FOLDS, len(lams))), np.zeros((FOLDS, len(lams)))
    for k in range(FOLDS):
        tr, va = f != k, f == k
        Za, Zb, _, _ = standardize(X[~test][tr], X[~test][va])
        m = ytr[tr].mean()
        for i, l_ in enumerate(lams):
            w = ridge_svd(Za, ytr[tr] - m, l_)
            pr = Zb @ w + m
            mse[k, i] = float(((pr - ytr[va]) ** 2).mean())
            acc[k, i] = acc_of(pr, ytr[va])
    mm = mse.mean(0)
    best = int(np.argmin(mm))
    se = mse.std(0, ddof=1) / math.sqrt(FOLDS)
    one_se = int(max(i for i in range(len(lams)) if mm[i] <= mm[best] + se[best]))
    test_acc = [acc_of(Zte @ ridge_svd(Ztr, yc, l_) + ytr.mean(), y[test]) for l_ in lams]
    coef = np.array([ridge_svd(Ztr, yc, l_) for l_ in lams])
    return dict(d=d, lams=lams, shows=shows, shrink=shrink, df=df, uy=uy, cv_mse=mm, cv_mse_se=se, cv_acc=acc.mean(0),
                cv_acc_sd=acc.std(0, ddof=1), best=best, one_se=one_se, lam_best=float(lams[best]),
                test_acc=np.array(test_acc), coef=coef, d_ratio=float(d[0] / d[-1]))


# ---------------------------------------------------------------------------
def soft(z, t):
    return np.sign(z) * np.maximum(np.abs(z) - t, 0.0)


def enet_cd(Z, yc, lam, alpha=1.0, w=None, tol=1e-9, max_sweeps=5000):
    """Coordinate descent for (1/2n)|yc - Zw|^2 + lam (alpha |w|_1 + (1 - alpha)/2 |w|^2), Z standardized (each
    column has mean 0 and mean square 1), yc centred.  Each coordinate's exact minimizer is a soft threshold."""
    n, p = Z.shape
    w = np.zeros(p) if w is None else w.copy()
    r = yc - Z @ w
    for sweep in range(max_sweeps):
        big = 0.0
        for j in range(p):
            zj = Z[:, j]
            rho = zj @ r / n + w[j]  # the coordinate's least-squares value, with the others held fixed
            new = soft(rho, lam * alpha) / (1 + lam * (1 - alpha))
            if new != w[j]:
                r -= zj * (new - w[j])
                big = max(big, abs(new - w[j]))
                w[j] = new
        if big < tol:
            break
    return w, sweep + 1


def compute_lasso():
    p = load("pages")
    vocab = p["vocab"]
    X, y, test, _ = split()
    Ztr, Zte, _, _ = standardize(X[~test], X[test])
    ytr = y[~test].astype(float)
    m = ytr.mean()
    yc = ytr - m
    n = len(yc)
    lam_max = float(np.abs(Ztr.T @ yc).max() / n)
    lams = lam_max * np.logspace(0, -3, 61)
    path, sweeps, kkt = [], [], 0.0
    w = np.zeros(Ztr.shape[1])
    for lam in lams:
        w, s = enet_cd(Ztr, yc, lam, w=w)
        path.append(w.copy())
        sweeps.append(s)
        g = Ztr.T @ (yc - Ztr @ w) / n  # KKT: |g_j| <= lam where w_j = 0, g_j = lam sign(w_j) where w_j != 0
        on = w != 0
        kkt = max(kkt, float(np.max(np.abs(g[~on])) - lam) if (~on).any() else 0.0,
                  float(np.max(np.abs(g[on] - lam * np.sign(w[on])))) if on.any() else 0.0)
    path = np.array(path)
    assert kkt < 1e-6, kkt
    order = []
    for k in range(len(lams)):
        for i in np.nonzero(path[k])[0]:
            if vocab[i] not in order:
                order.append(vocab[i])
    nnz = (path != 0).sum(1)
    test_acc = np.array([acc_of(Zte @ w_ + m, y[test]) for w_ in path])
    # ten-fold cross-validation on the training pages
    f = kfold(ytr, seed=1996)
    mse = np.zeros((FOLDS, len(lams)))
    acc = np.zeros((FOLDS, len(lams)))
    for k in range(FOLDS):
        tr, va = f != k, f == k
        Za, Zb, _, _ = standardize(X[~test][tr], X[~test][va])
        ma = ytr[tr].mean()
        w = np.zeros(Za.shape[1])
        for i, lam in enumerate(lams):
            w, _ = enet_cd(Za, ytr[tr] - ma, lam, w=w, tol=1e-7)
            pr = Zb @ w + ma
            mse[k, i] = float(((pr - ytr[va]) ** 2).mean())
            acc[k, i] = acc_of(pr, ytr[va])
    mm, se = mse.mean(0), mse.std(0, ddof=1) / math.sqrt(FOLDS)
    best = int(np.argmin(mm))
    one_se = int(min(i for i in range(len(lams)) if mm[i] <= mm[best] + se[best]))
    sel = [vocab[i] for i in np.argsort(-np.abs(path[one_se])) if path[one_se][i] != 0]
    # the elastic net (alpha = 1/2): the same path, and a correlated pair of words
    epath = []
    w = np.zeros(Ztr.shape[1])
    for lam in lams:
        w, _ = enet_cd(Ztr, yc, lam, alpha=0.5, w=w)
        epath.append(w.copy())
    epath = np.array(epath)
    Cm = np.corrcoef(Ztr.T)
    np.fill_diagonal(Cm, 0)
    # the most correlated pair of words both of which matter: the elastic net keeps them together
    best_pair, best_score = None, -1
    for i in range(len(vocab)):
        for j in range(i + 1, len(vocab)):
            if Cm[i, j] < 0.5:
                continue
            gap = abs(np.argmax(path[:, i] != 0) - np.argmax(path[:, j] != 0)) if (path[:, i] != 0).any() and (
                path[:, j] != 0).any() else 99
            gap_e = abs(np.argmax(epath[:, i] != 0) - np.argmax(epath[:, j] != 0)) if (epath[:, i] != 0).any() and (
                epath[:, j] != 0).any() else 99
            score = Cm[i, j] * (gap - gap_e)
            if score > best_score:
                best_pair, best_score = (i, j), score
    # twins: add a near-copy of "not" (its rate plus a little noise).  The lasso picks one twin; the elastic net
    # shares the weight between them.
    j = vocab.index("not")
    gt = rng(2005)  # Zou & Hastie, 2005
    twin = Ztr[:, j] + 0.1 * gt.standard_normal(len(Ztr))
    twin = (twin - twin.mean()) / twin.std()
    Zt = np.hstack([Ztr, twin[:, None]])
    tw_l, tw_e = [], []
    wl, we = np.zeros(Zt.shape[1]), np.zeros(Zt.shape[1])
    for lam in lams:
        wl, _ = enet_cd(Zt, yc, lam, w=wl)
        we, _ = enet_cd(Zt, yc, lam, alpha=0.5, w=we)
        tw_l.append([wl[j], wl[-1]])
        tw_e.append([we[j], we[-1]])
    k8 = int(np.argmax(nnz >= 8))
    return dict(twin_lasso=np.array(tw_l), twin_enet=np.array(tw_e), twin_corr=float(np.corrcoef(Ztr[:, j], twin)[0, 1]),
                k8=k8, acc8=float(test_acc[k8]), words8=[vocab[i] for i in np.nonzero(path[k8])[0]],
                lams=lams, lam_max=lam_max, path=path, nnz=nnz, sweeps=sweeps, kkt=kkt, order=order[:12],
                test_acc=test_acc, cv_mse=mm, cv_se=se, cv_acc=acc.mean(0), cv_acc_sd=acc.std(0, ddof=1), best=best,
                one_se=one_se, selected=sel, n_selected=len(sel), acc_one_se=float(test_acc[one_se]),
                acc_best=float(test_acc[best]), epath=epath, enet_nnz=(epath != 0).sum(1),
                pair=[vocab[best_pair[0]], vocab[best_pair[1]]] if best_pair else [],
                pair_idx=list(best_pair) if best_pair else [], pair_corr=float(Cm[best_pair]) if best_pair else 0.0)


# ---------------------------------------------------------------------------
def sigmoid(z):
    return 0.5 * (1 + np.tanh(0.5 * np.asarray(z)))


def logloss(z, y):
    """Mean cross-entropy (nats) of log-odds z against 0/1 labels y, computed stably."""
    z = np.asarray(z, float)
    return float(np.mean(np.logaddexp(0, z) - y * z))


def logreg(X, y, l2=0.0, l1=0.0, w0=None, iters=3000, lr=None):
    """Logistic regression by (proximal) gradient descent; X standardized; returns (w, b).  The step is 1 / L, the
    gradient's Lipschitz constant, unless given."""
    n, d = X.shape
    if lr is None:
        lr = 1 / (0.25 * (np.linalg.norm(X, 2) ** 2 / n + 1) + l2)
    w = np.zeros(d) if w0 is None else w0[0].copy()
    b = 0.0 if w0 is None else w0[1]
    for _ in range(iters):
        p = sigmoid(X @ w + b)
        gw = X.T @ (p - y) / n + l2 * w
        gb = float((p - y).mean())
        w = w - lr * gw
        b -= lr * gb
        if l1:
            w = np.sign(w) * np.maximum(np.abs(w) - lr * l1, 0)
    return w, b


def newton_logreg(X, y, l2=1e-2, iters=50, tol=1e-12, history=False):
    """Newton's method (iteratively reweighted least squares) for mean cross-entropy + l2/2 |w|^2 (the intercept is
    not penalized).  Returns (w, b), and with ``history`` the loss after every step."""
    n, d = X.shape
    A = np.hstack([X, np.ones((n, 1))])
    th = np.zeros(d + 1)
    pen = np.full(d + 1, l2)
    pen[-1] = 0.0
    hist = []

    def obj(t):
        return logloss(A @ t, y) + 0.5 * float((pen * t * t).sum())

    hist.append(obj(th))
    for _ in range(iters):
        z = A @ th
        p = sigmoid(z)
        s = p * (1 - p)
        g = A.T @ (p - y) / n + pen * th
        H = (A * s[:, None]).T @ A / n + np.diag(pen) + 1e-12 * np.eye(d + 1)
        step = np.linalg.solve(H, g)
        t, f0 = 1.0, hist[-1]
        while obj(th - t * step) > f0 + 1e-15 and t > 1e-8:  # a safeguard; a full step is almost always taken
            t *= 0.5
        th = th - t * step
        hist.append(obj(th))
        if abs(hist[-2] - hist[-1]) < tol:
            break
    return (th[:-1], float(th[-1]), hist) if history else (th[:-1], float(th[-1]))


def compute_logistic():
    X, y, test, X2 = split()
    Z2tr, Z2te, mu, sd = standardize(X2[~test], X2[test])
    w, b = newton_logreg(Z2tr, y[~test].astype(float), l2=0.0)
    acc2 = acc_of(sigmoid(Z2te @ w + b), y[test])
    Ztr, Zte, _, _ = standardize(X[~test], X[test])
    W, B = newton_logreg(Ztr, y[~test].astype(float), l2=1e-2)
    acc70 = acc_of(sigmoid(Zte @ W + B), y[test])
    xs, ys, G = grid2(X2)
    prob = sigmoid(((G - mu) / sd) @ w + b).reshape(len(ys), len(xs))
    wr = w / sd
    b_raw = b - float(wr @ mu)
    ytr = y[~test].astype(float)
    loss = logloss(Z2tr @ w + b, ytr)
    # convexity at the answer: the Hessian X^T S X / n has only positive eigenvalues
    A = np.hstack([Z2tr, np.ones((len(Z2tr), 1))])
    p = sigmoid(A @ np.r_[w, b])
    H = (A * (p * (1 - p))[:, None]).T @ A / len(A)
    eig = np.linalg.eigvalsh(H)
    # how it learns: plain gradient descent from zero, its line (in the original units) and its loss along the way
    n = len(ytr)
    lr = 1 / (0.25 * (np.linalg.norm(Z2tr, 2) ** 2 / n + 1))
    wt, bt = np.zeros(2), 0.0
    keep = {0, 1, 2, 3, 5, 8, 12, 20, 35, 60, 100, 180, 320, 600, 1200, 4000}
    path, curve = [], []
    for it in range(4001):
        ce = logloss(Z2tr @ wt + bt, ytr) / math.log(2)
        curve.append((it, ce))
        if it in keep:
            path.append((it, *(wt / sd), bt - float((wt / sd) @ mu), ce))
        if it == 4000:
            break
        pz = sigmoid(Z2tr @ wt + bt)
        wt, bt = wt - lr * Z2tr.T @ (pz - ytr) / n, bt - lr * float((pz - ytr).mean())
    assert acc70 > acc2 > 0.75 and eig.min() > 0
    return dict(w=wr, b=b_raw, acc2=acc2, acc70=acc70, xs=xs, ys=ys, prob=prob, loss_bits=loss / math.log(2),
                path=np.array(path), curve=np.array(curve[::5] + [curve[-1]]), hess_eig=eig, n_te=int(test.sum()))


# ---------------------------------------------------------------------------
def compute_irls():
    """Newton (IRLS) against gradient descent, on the 70 rates; the 2-rate lines after each Newton step; and the
    unpenalized fit on all 70 rates, whose weights grow without end if the pages can be separated."""
    X, y, test, X2 = split()
    Ztr, Zte, _, _ = standardize(X[~test], X[test])
    ytr = y[~test].astype(float)
    l2 = 1e-2
    w, b, hist = newton_logreg(Ztr, ytr, l2=l2, history=True)
    fstar = hist[-1]
    n, d = Ztr.shape
    A = np.hstack([Ztr, np.ones((n, 1))])
    L = 0.25 * np.linalg.norm(A, 2) ** 2 / n + l2
    th = np.zeros(d + 1)
    pen = np.full(d + 1, l2)
    pen[-1] = 0
    gd = []
    for it in range(20001):
        z = A @ th
        if it in (0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000) or it % 250 == 0:
            gd.append((it, logloss(z, ytr) + 0.5 * float((pen * th * th).sum()) - fstar))
        th = th - (A.T @ (sigmoid(z) - ytr) / n + pen * th) / L
    newton_gap = [max(h - fstar, 0.0) for h in hist]
    # the 2-rate picture: Newton's lines after 0..5 steps, and gradient descent's after the same number of steps
    Z2tr, _, mu, sd = standardize(X2[~test], X2[test])
    lines_n, lines_g = [], []
    A2 = np.hstack([Z2tr, np.ones((n, 1))])
    tn, tg = np.zeros(3), np.zeros(3)
    L2 = 0.25 * np.linalg.norm(A2, 2) ** 2 / n
    for k in range(7):
        for t_, out in ((tn, lines_n), (tg, lines_g)):
            wr = t_[:2] / sd
            out.append([float(wr[0]), float(wr[1]), float(t_[2] - wr @ mu), logloss(A2 @ t_, ytr) / math.log(2)])
        p = sigmoid(A2 @ tn)
        s = p * (1 - p)
        H = (A2 * s[:, None]).T @ A2 / n
        tn = tn - np.linalg.solve(H, A2.T @ (p - ytr) / n)
        tg = tg - (A2.T @ (sigmoid(A2 @ tg) - ytr) / n) / L2
    # no penalty: is the training set separable with 70 rates?  Shrink the penalty and watch the weights
    pens = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7]
    norms, train_acc, losses = [], [], []
    for p_ in pens:
        w_, b_ = newton_logreg(Ztr, ytr, l2=p_, iters=200)
        norms.append(float(np.linalg.norm(w_)))
        train_acc.append(acc_of(Ztr @ w_ + b_, ytr, 0.0))
        losses.append(logloss(Ztr @ w_ + b_, ytr) / math.log(2))
    separable = train_acc[-1] == 1.0
    return dict(newton_gap=newton_gap, n_newton=len(hist) - 1, gd=np.array(gd), fstar=fstar, l2=l2,
                lines_newton=lines_n, lines_gd=lines_g, pens=pens, norms=norms, train_acc=train_acc,
                losses=losses, separable=bool(separable), acc_test=acc_of(Zte @ w + b, y[test], 0.0),
                gd_iters_to=int(next((int(i) for i, gp in gd if gp < 1e-6), -1)), cond_H=float(np.linalg.cond(
                    (A * (sigmoid(A @ np.r_[w, b]) * (1 - sigmoid(A @ np.r_[w, b])))[:, None]).T @ A / n + np.diag(pen))))


# ---------------------------------------------------------------------------
def nb_fit(C, y, alpha=1.0):
    """Multinomial naive Bayes on word counts: returns (weights, bias) of its log-odds, a linear function."""
    tA = C[y == 0].sum(0) + alpha
    tD = C[y == 1].sum(0) + alpha
    w = np.log(tD / tD.sum()) - np.log(tA / tA.sum())
    pi = (y == 1).mean()
    return w, float(math.log(pi / (1 - pi)))


def reliability(p, y, bins=10):
    e = np.linspace(0, 1, bins + 1)
    k = np.clip(np.digitize(p, e[1:-1]), 0, bins - 1)
    cnt = np.bincount(k, minlength=bins).astype(float)
    conf = np.bincount(k, weights=p, minlength=bins) / np.maximum(cnt, 1)
    frac = np.bincount(k, weights=y, minlength=bins) / np.maximum(cnt, 1)
    ece = float((cnt * np.abs(conf - frac)).sum() / cnt.sum())
    return dict(count=cnt, conf=conf, frac=frac, ece=ece, brier=float(((p - y) ** 2).mean()),
                logloss=float(-np.mean(y * np.log(np.clip(p, 1e-12, 1)) + (1 - y) * np.log(np.clip(1 - p, 1e-12, 1)))))


def platt(z, y):
    """Fit p = sigmoid(a z + c) to scores z: one-feature logistic regression."""
    w, b = newton_logreg(np.asarray(z, float)[:, None], y.astype(float), l2=0.0)
    return float(w[0]), b


def compute_calibration():
    """Cross-validated probabilities for every page (ten folds): are they honest?"""
    X, y, test, X2 = split()
    f = kfold(y, seed=1950)
    yf = y.astype(float)
    P = {k: np.zeros(len(y)) for k in ("lr2", "lr70", "nb", "nb_platt")}
    Znb = np.zeros(len(y))
    for k in range(FOLDS):
        tr, va = f != k, f == k
        a, b_, _, _ = standardize(X2[tr], X2[va])
        w, c = newton_logreg(a, yf[tr], l2=0.0)
        P["lr2"][va] = sigmoid(b_ @ w + c)
        a, b_, _, _ = standardize(X[tr], X[va])
        w, c = newton_logreg(a, yf[tr], l2=1e-2)
        P["lr70"][va] = sigmoid(b_ @ w + c)
        w, c = nb_fit(X[tr], y[tr])
        z = X[va] @ w + c
        Znb[va] = z
        P["nb"][va] = sigmoid(z)
        # Platt scaling, fitted on this fold's training pages only (their own cross-validated scores)
        f2 = kfold(y[tr], k=5, seed=1999 + k)
        zt = np.zeros(tr.sum())
        for j in range(5):
            w2, c2 = nb_fit(X[tr][f2 != j], y[tr][f2 != j])
            zt[f2 == j] = X[tr][f2 == j] @ w2 + c2
        sa, sc = platt(zt, y[tr])
        P["nb_platt"][va] = sigmoid(sa * z + sc)
    out = {k: reliability(v, yf) for k, v in P.items()}
    out["acc"] = {k: acc_of(v, y) for k, v in P.items()}
    out["nb_z"] = Znb
    out["nb_extreme"] = float((np.abs(Znb) > math.log(1e6)).mean())  # beyond a million to one
    out["nb_median_abs_z"] = float(np.median(np.abs(Znb)))
    for k, v in P.items():
        out[f"p_{k}"] = v
    return out


# ---------------------------------------------------------------------------
NB_SIZES = [4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 352, 448]


def compute_nbvslr():
    """Ng & Jordan (2002) on the pages: naive Bayes against logistic regression, trained on m random training pages
    (both authors present), tested on the held-out pages; many draws per m."""
    X, y, test, _ = split()
    Xtr, ytr, Xte, yte = X[~test], y[~test], X[test], y[test]
    g = rng(2002)
    err_nb, err_lr = {}, {}
    for m in NB_SIZES:
        reps = 1 if m == len(ytr) else (200 if m <= 64 else 60)
        a, b = [], []
        for _ in range(reps):
            while True:
                idx = g.choice(len(ytr), m, replace=False) if m < len(ytr) else np.arange(len(ytr))
                if 0 < ytr[idx].sum() < m:
                    break
            w, c = nb_fit(Xtr[idx], ytr[idx])
            a.append(1 - acc_of(Xte @ w + c, yte, 0.0))
            Za, Zb, _, _ = standardize(Xtr[idx], Xte)
            w, c = newton_logreg(Za, ytr[idx].astype(float), l2=1e-2)
            b.append(1 - acc_of(Zb @ w + c, yte, 0.0))
        err_nb[str(m)], err_lr[str(m)] = a, b

    def summ(e):
        return {k: dict(mean=float(np.mean(v)), lo=float(np.percentile(v, 10)), hi=float(np.percentile(v, 90)),
                        se=float(np.std(v) / math.sqrt(max(len(v), 1)))) for k, v in e.items()}

    nb, lr = summ(err_nb), summ(err_lr)
    better = [m for m in NB_SIZES if nb[str(m)]["mean"] < lr[str(m)]["mean"]]
    cross = next((m for m in NB_SIZES if lr[str(m)]["mean"] < nb[str(m)]["mean"]
                  and all(lr[str(k)]["mean"] <= nb[str(k)]["mean"] for k in NB_SIZES if k >= m)), None)
    return dict(sizes=NB_SIZES, nb=nb, lr=lr, nb_better_at=better, crossover=cross)


# ---------------------------------------------------------------------------
def gen_eig(SB, SW):
    """The generalized eigenproblem S_B w = lam S_W w, through the Cholesky factor of S_W."""
    Lc = np.linalg.cholesky(SW)
    Li = np.linalg.inv(Lc)
    M = Li @ SB @ Li.T
    vals, vecs = np.linalg.eigh(M)
    w = Li.T @ vecs[:, -1]
    return vals[::-1], w / np.linalg.norm(w)


def compute_lda():
    X, y, test, X2 = split()
    A, D = X2[~test][y[~test] == 0], X2[~test][y[~test] == 1]
    Sw = np.cov(A.T) * (len(A) - 1) + np.cov(D.T) * (len(D) - 1)
    w = np.linalg.solve(Sw, D.mean(0) - A.mean(0))
    w /= np.linalg.norm(w)
    angles = np.linspace(0, math.pi, 181)

    def J(u):
        pa, pd = A @ u, D @ u
        return (pd.mean() - pa.mean()) ** 2 / (pa.var() + pd.var())

    sep = np.array([J(np.array([math.cos(a), math.sin(a)])) for a in angles])
    best = float(math.atan2(w[1], w[0]) % math.pi)
    assert abs(angles[np.argmax(sep)] - best) < 0.03 or abs(abs(angles[np.argmax(sep)] - best) - math.pi) < 0.03
    c = float(0.5 * ((A @ w).mean() + (D @ w).mean()))
    acc = acc_of(X2[test] @ w, y[test], c)
    # the generalized eigenproblem, on the 70 standardized rates
    Ztr, Zte, _, _ = standardize(X[~test], X[test])
    ytr = y[~test]
    ZA, ZD = Ztr[ytr == 0], Ztr[ytr == 1]
    dm = ZD.mean(0) - ZA.mean(0)
    SB = np.outer(dm, dm)
    SW = (ZA - ZA.mean(0)).T @ (ZA - ZA.mean(0)) + (ZD - ZD.mean(0)).T @ (ZD - ZD.mean(0))
    vals, we = gen_eig(SB, SW)
    wf = np.linalg.solve(SW, dm)
    wf /= np.linalg.norm(wf)
    cos_eig = float(abs(we @ wf))
    if we @ dm < 0:
        we = -we
    rq = float((we @ SB @ we) / (we @ SW @ we))  # the Rayleigh quotient at the eigenvector = the top eigenvalue
    # least squares on a 0/1 target points the same way (two classes)
    yc = ytr - ytr.mean()
    wls = np.linalg.lstsq(Ztr, yc, rcond=None)[0]
    cos_ls = float(abs(wls @ wf) / np.linalg.norm(wls))
    cut = 0.5 * ((ZA @ we).mean() + (ZD @ we).mean())
    acc70 = acc_of(Zte @ we, y[test], cut)
    p = load("pages")
    top = [p["vocab"][i] for i in np.argsort(-np.abs(we))[:6]]
    signs = [int(np.sign(we[i])) for i in np.argsort(-np.abs(we))[:6]]
    rank_SB = int(np.linalg.matrix_rank(SB))
    return dict(w=w, c=c, angles=angles, sep=sep, best=best, acc2=acc, mA=A.mean(0), mD=D.mean(0),
                covA=np.cov(A.T), covD=np.cov(D.T), eigvals=vals[:5], cos_eig=cos_eig, rq=rq, cos_ls=cos_ls,
                acc70=acc70, top=top, top_signs=signs, rank_SB=rank_SB)


# ---------------------------------------------------------------------------
def knn_scores(Ztr, ytr, Q, k):
    d = ((Q[:, None, :] - Ztr[None]) ** 2).sum(-1)
    o = np.argsort(d, 1, kind="stable")[:, :k]
    return ytr[o].mean(1)


KS = [1, 3, 5, 9, 15, 25, 45, 75, 125, 201]


def compute_knn():
    X, y, test, X2 = split()
    Z2tr, Z2te, mu, sd = standardize(X2[~test], X2[test])
    ytr = y[~test]
    xs, ys, G = grid2(X2)
    Gz = (G - mu) / sd
    out = dict(xs=xs, ys=ys, ks=KS)
    for k in KS:
        out[f"acc{k}"] = acc_of(knn_scores(Z2tr, ytr, Z2te, k), y[test])
        out[f"train{k}"] = acc_of(knn_scores(Z2tr, ytr, Z2tr, k), ytr)
        out[f"region{k}"] = knn_scores(Z2tr, ytr, Gz, k).reshape(len(ys), len(xs))
    f = kfold(ytr, seed=1967)
    cv = np.zeros((FOLDS, len(KS)))
    for j in range(FOLDS):
        a, b, _, _ = standardize(X2[~test][f != j], X2[~test][f == j])
        for i, k in enumerate(KS):
            cv[j, i] = acc_of(knn_scores(a, ytr[f != j], b, k), ytr[f == j])
    out["cv"], out["cv_sd"] = cv.mean(0), cv.std(0, ddof=1)
    out["k_cv"] = int(KS[int(np.argmax(cv.mean(0)))])
    out["acc_kcv"] = out[f"acc{out['k_cv']}"]
    return out


# ---------------------------------------------------------------------------
CH_MU = 0.8  # two unit Gaussians at -0.8 and +0.8 on the first axis


def compute_coverhart():
    """1-NN on two overlapping Gaussians, against the Bayes error R* and the Cover-Hart limit."""
    from math import erf, sqrt

    Phi = lambda t: 0.5 * (1 + erf(t / sqrt(2)))  # noqa: E731
    Rstar = Phi(-CH_MU)
    # the 1-NN limit: E[2 eta (1 - eta)], eta(x) = P(class 1 | x); only the first coordinate matters
    t = np.linspace(-9, 9, 200001)
    pdf = lambda u: np.exp(-u * u / 2) / sqrt(2 * math.pi)  # noqa: E731
    p0, p1 = pdf(t + CH_MU), pdf(t - CH_MU)
    eta = p1 / (p0 + p1)
    mix = 0.5 * (p0 + p1)
    lim1 = float(np.trapezoid(2 * eta * (1 - eta) * mix, t))
    bound = 2 * Rstar * (1 - Rstar)
    g = rng(1967)
    ns = [10, 30, 100, 300, 1000, 3000, 10000]
    reps = {10: 200, 30: 200, 100: 100, 300: 60, 1000: 60, 3000: 40, 10000: 30}
    nte = 4000
    e1, ek = {}, {}
    for n in ns:
        a, b = [], []
        for _ in range(reps[n]):
            yt = g.integers(0, 2, n)
            Xt = g.standard_normal((n, 2))
            Xt[:, 0] += np.where(yt == 1, CH_MU, -CH_MU)
            yq = g.integers(0, 2, nte)
            Xq = g.standard_normal((nte, 2))
            Xq[:, 0] += np.where(yq == 1, CH_MU, -CH_MU)
            k = max(1, int(round(math.sqrt(n))) | 1)
            e_1, e_k = 0, 0
            for s in range(0, nte, 500):
                d = ((Xq[s:s + 500, None] - Xt[None]) ** 2).sum(-1)
                nn1 = np.argmin(d, 1)
                e_1 += int((yt[nn1] != yq[s:s + 500]).sum())
                ok = np.argpartition(d, k - 1, 1)[:, :k]
                e_k += int(((yt[ok].mean(1) > 0.5) != yq[s:s + 500]).sum())
            a.append(e_1 / nte)
            b.append(e_k / nte)
        e1[str(n)] = dict(mean=float(np.mean(a)), lo=float(np.percentile(a, 10)), hi=float(np.percentile(a, 90)))
        ek[str(n)] = dict(mean=float(np.mean(b)), lo=float(np.percentile(b, 10)), hi=float(np.percentile(b, 90)))
    return dict(mu=CH_MU, Rstar=float(Rstar), lim1=lim1, bound=float(bound), ns=ns, e1=e1, ek=ek)


# ---------------------------------------------------------------------------
CURSE_D = [1, 2, 3, 5, 10, 20, 50, 100, 200, 500, 1000]


def compute_curse():
    g = rng(1957)  # Bellman, Dynamic Programming, 1957
    contrast, nn_frac = [], []
    for d in CURSE_D:
        P = g.random((2000, d))
        Q = g.random((50, d))
        D = np.sqrt(((Q[:, None] - P[None]) ** 2).sum(-1))
        contrast.append(float(np.mean((D.max(1) - D.min(1)) / D.min(1))))
        nn_frac.append(float(np.mean(D.min(1) / D.mean(1))))
    # the pages: 15-NN and logistic regression as pure-noise columns are added to the 70 rates
    X, y, test, _ = split()
    noise = [0, 10, 30, 100, 300, 1000]
    knn_acc, lr_acc = {}, {}
    for m in noise:
        a, b = [], []
        for s in range(5 if m else 1):
            gg = rng(100 + s)
            N = gg.standard_normal((len(y), m))
            Xn = np.hstack([X, N])
            Za, Zb, _, _ = standardize(Xn[~test], Xn[test])
            a.append(acc_of(knn_scores(Za, y[~test], Zb, 15), y[test]))
            w, c = newton_logreg(Za, y[~test].astype(float), l2=1e-1)
            b.append(acc_of(Zb @ w + c, y[test], 0.0))
        knn_acc[str(m)] = dict(mean=float(np.mean(a)), lo=float(np.min(a)), hi=float(np.max(a)))
        lr_acc[str(m)] = dict(mean=float(np.mean(b)), lo=float(np.min(b)), hi=float(np.max(b)))
    edge = {str(d): 0.1 ** (1 / d) for d in CURSE_D}  # the side of a cube holding 10% of uniform data
    return dict(dims=CURSE_D, contrast=contrast, nn_frac=nn_frac, noise=noise, knn=knn_acc, lr=lr_acc, edge=edge)


# ---------------------------------------------------------------------------
def toy_ring(seed=8):
    g = np.random.default_rng(seed)
    r_in, r_out = g.uniform(0, 0.9, 40), g.uniform(1.5, 2.1, 60)
    t_in, t_out = g.uniform(0, 2 * math.pi, 40), g.uniform(0, 2 * math.pi, 60)
    P = np.vstack([np.stack([r_in * np.cos(t_in), r_in * np.sin(t_in)], 1),
                   np.stack([r_out * np.cos(t_out), r_out * np.sin(t_out)], 1)])
    return P, np.array([0] * 40 + [1] * 60)


def toy_clusters(seed=7):
    g = np.random.default_rng(seed)
    A = g.normal([-1.3, -0.6], 0.45, (14, 2))
    B = g.normal([1.2, 0.8], 0.45, (14, 2))
    return np.vstack([A, B]), np.array([0] * 14 + [1] * 14)


def rbf(P, Q, gamma):
    return np.exp(-gamma * ((P[:, None, :] - Q[None]) ** 2).sum(-1))


def compute_kernel():
    out = {}
    # the lift: (x1, x2) -> (x1, x2, x1^2 + x2^2); a hard-margin linear SVM in 3D finds a plane
    P, y = toy_ring()
    L = np.hstack([P, (P ** 2).sum(1, keepdims=True)])
    s = smo(L @ L.T, y, C=1e6)
    w = (s["alpha"] * (2 * y - 1)) @ L
    out.update(lift_w=w, lift_b=s["b"], lift_sv=s["sv"], lift_sep=bool(np.all(np.sign(L @ w + s["b"]) == 2 * y - 1)))
    # a polynomial kernel is a dot product of explicit features
    g = rng(1909)  # Mercer, 1909
    x, z = g.standard_normal((1000, 2)), g.standard_normal((1000, 2))

    def phi(v):
        a, b = v[:, 0], v[:, 1]
        r2 = math.sqrt(2)
        return np.stack([a * a, b * b, r2 * a * b, r2 * a, r2 * b, np.ones_like(a)], 1)

    out["poly_err"] = float(np.abs(((x * z).sum(1) + 1) ** 2 - (phi(x) * phi(z)).sum(1)).max())
    # Mercer: Gram matrices of the Gaussian kernel have no negative eigenvalues; a "sigmoid kernel" can
    X, yy, test, X2 = split()
    Z2, _, _, _ = standardize(X2[~test], X2[test])
    Z70, _, _, _ = standardize(X[~test], X[test])
    ev2 = np.linalg.eigvalsh(rbf(Z2, Z2, 1.0))
    ev70 = np.linalg.eigvalsh(rbf(Z70, Z70, 1 / 70))
    evs = np.linalg.eigvalsh(np.tanh(1.0 * Z2 @ Z2.T - 1.0))
    out.update(ev2=ev2[::-1], ev70=ev70[::-1], ev_sig=evs[::-1], min_ev2=float(ev2.min()), min_ev70=float(ev70.min()),
               min_sig=float(evs.min()), n_neg_sig=int((evs < -1e-9).sum()), n=len(Z2))
    # the Gaussian kernel's features: e^{-g(x-z)^2} = e^{-gx^2} e^{-gz^2} sum_k (2g)^k x^k z^k / k!, truncated
    xs = np.linspace(-1.5, 1.5, 61)
    gam = 1.0
    errs = []
    for D in range(1, 21):
        k = np.arange(D)
        fx = np.exp(-gam * xs[:, None] ** 2) * np.sqrt((2 * gam) ** k / np.array([math.factorial(int(i)) for i in k])) * xs[:, None] ** k
        approx = fx @ fx.T
        errs.append(float(np.abs(approx - np.exp(-gam * (xs[:, None] - xs[None]) ** 2)).max()))
    out["taylor_err"] = errs
    # the representer theorem: ridge in an explicit 2,000-feature space (random Fourier features of the Gaussian
    # kernel) has its answer in the span of the n data points' features
    Dm = 2000
    Wf = g.standard_normal((2, Dm)) * math.sqrt(2 * 1.0)
    bf = g.uniform(0, 2 * math.pi, Dm)
    F = math.sqrt(2 / Dm) * np.cos(Z2 @ Wf + bf)
    t = 2.0 * yy[~test] - 1
    lam = 1.0
    wprim = np.linalg.solve(F.T @ F + lam * np.eye(Dm), F.T @ t)
    alpha = np.linalg.solve(F @ F.T + lam * np.eye(len(t)), t)
    out["rep_err"] = float(np.abs(wprim - F.T @ alpha).max() / np.abs(wprim).max())
    # projection of w onto the span of the data's features: what is left over
    Qf, _ = np.linalg.qr(F.T)
    out["rep_resid"] = float(np.linalg.norm(wprim - Qf @ (Qf.T @ wprim)) / np.linalg.norm(wprim))
    out["rep_dims"] = Dm
    # kernel ridge with the exact kernel on the pages: accuracy
    K = rbf(Z2, Z2, 1.0)
    a2 = np.linalg.solve(K + lam * np.eye(len(t)), t)
    _, Z2te, _, _ = standardize(X2[~test], X2[test])
    out["krr_acc"] = acc_of(rbf(Z2te, Z2, 1.0) @ a2, yy[test], 0.0)
    # XOR: no line separates it; the perceptron never stops making mistakes
    Pxor = np.array([[1.0, 1.0], [-1.0, -1.0], [1.0, -1.0], [-1.0, 1.0]])
    txor = np.array([1, 1, -1, -1.0])
    wv, mistakes = np.zeros(3), 0
    for ep in range(100):
        for i in range(4):
            xa = np.r_[Pxor[i], 1.0]
            if txor[i] * (wv @ xa) <= 0:
                wv += txor[i] * xa
                mistakes += 1
    out["xor_mistakes_100"] = mistakes
    # ...and in the lifted space (x1, x2, x1 x2) it separates in a few passes
    wv, mk, ep_done = np.zeros(4), 0, None
    for ep in range(100):
        bad = 0
        for i in range(4):
            xa = np.r_[Pxor[i], Pxor[i, 0] * Pxor[i, 1], 1.0]
            if txor[i] * (wv @ xa) <= 0:
                wv += txor[i] * xa
                mk += 1
                bad += 1
        if bad == 0:
            ep_done = ep
            break
    out["xor_lift_mistakes"], out["xor_lift_epochs"] = mk, ep_done
    return out


# ---------------------------------------------------------------------------
def smo(K, y, C, tol=1e-4, max_iter=200000):
    """Sequential minimal optimization for the soft-margin SVM dual (Platt 1998; the working-set rule of Fan, Chen &
    Lin 2005, as in LIBSVM):  minimize 1/2 a'Qa - sum(a)  with  0 <= a <= C,  sum(a_i t_i) = 0,  Q = t t' * K.
    Returns the alphas, the bias, the support vectors, the dual objective and the iterations."""
    t = 2.0 * np.asarray(y) - 1
    n = len(t)
    Q = K * t[:, None] * t[None]
    a = np.zeros(n)
    G = -np.ones(n)  # the gradient Qa - 1
    diag = np.diag(Q).copy()
    it = 0
    for it in range(max_iter):
        up = ((t > 0) & (a < C)) | ((t < 0) & (a > 0))
        low = ((t > 0) & (a > 0)) | ((t < 0) & (a < C))
        v = -t * G
        i = int(np.argmax(np.where(up, v, -np.inf)))
        m_up = v[i]
        M_low = np.min(np.where(low, v, np.inf))
        if m_up - M_low < tol:
            break
        # second-order choice of j among the lower set
        bij = m_up - v
        aij = diag[i] + diag - 2 * Q[i] * t[i] * t  # K_ii + K_jj - 2 K_ij
        aij = np.where(aij > 1e-12, aij, 1e-12)
        cand = low & (v < m_up)
        j = int(np.argmax(np.where(cand, bij * bij / aij, -np.inf)))
        # solve the two-variable problem along t_i a_i + t_j a_j = const
        Kij = Q[i, j] * t[i] * t[j]
        eta = max(Q[i, i] + Q[j, j] - 2 * Kij, 1e-12)
        delta = (-t[i] * G[i] + t[j] * G[j]) / eta  # the step for t_i a_i (unclipped)
        ai_old, aj_old = a[i], a[j]
        # bounds on the step d, with a_i += t_i d, a_j -= t_j d
        lo_i, hi_i = (-ai_old, C - ai_old) if t[i] > 0 else (ai_old - C, ai_old)
        lo_j, hi_j = (aj_old - C, aj_old) if t[j] > 0 else (-aj_old, C - aj_old)
        d = min(max(delta, max(lo_i, lo_j)), min(hi_i, hi_j))
        a[i] = ai_old + t[i] * d
        a[j] = aj_old - t[j] * d
        a[i] = min(max(a[i], 0.0), C)
        a[j] = min(max(a[j], 0.0), C)
        G += Q[:, i] * (a[i] - ai_old) + Q[:, j] * (a[j] - aj_old)
    v = -t * G
    free = (a > 1e-8) & (a < C - 1e-8)
    if free.any():
        b = float(np.mean(v[free]))
    else:
        up = ((t > 0) & (a < C)) | ((t < 0) & (a > 0))
        low = ((t > 0) & (a > 0)) | ((t < 0) & (a < C))
        b = float(0.5 * (np.max(np.where(up, v, -np.inf)) + np.min(np.where(low, v, np.inf))))
    dual = float(a.sum() - 0.5 * a @ Q @ a)
    return dict(alpha=a, b=b, sv=np.nonzero(a > 1e-8)[0], free=np.nonzero(free)[0], dual=dual, iters=it + 1,
                gap_viol=float(m_up - M_low) if it + 1 < max_iter else float("nan"))


def svm_primal(K, y, a, b, C):
    """The primal objective 1/2 |w|^2 + C sum hinge, with w = sum a_i t_i phi(x_i) (so |w|^2 = a'Qa)."""
    t = 2.0 * np.asarray(y) - 1
    f = (a * t) @ K + b
    return float(0.5 * (a * t) @ K @ (a * t) + C * np.maximum(0, 1 - t * f).sum()), f


SVM_CS = [0.01, 0.1, 1.0, 10.0, 100.0]
SVM_GS = [0.1, 0.3, 1.0, 3.0, 10.0]


def compute_svm():
    out = {}
    # the separable toy: a hard margin, three or so support vectors, the street's width
    P, y = toy_clusters()
    s = smo(P @ P.T, y, C=1e6, tol=1e-8)
    t = 2.0 * y - 1
    w = (s["alpha"] * t) @ P
    out.update(toy_w=w, toy_b=s["b"], toy_sv=s["sv"], toy_margin=float(1 / np.linalg.norm(w)),
               toy_alpha=s["alpha"], toy_sum_at=float((s["alpha"] * t).sum()))
    # the perceptron on the same toy: how many mistakes, against Novikoff's (R / gamma)^2
    wv, mk = np.zeros(3), 0
    order = rng(1958).permutation(len(y))
    for ep in range(1000):
        bad = 0
        for i in order:
            xa = np.r_[P[i], 1.0]
            if t[i] * (wv @ xa) <= 0:
                wv += t[i] * xa
                mk += 1
                bad += 1
        if bad == 0:
            break
    # Novikoff with the bias folded in: R = max |(x, 1)|, gamma = the margin of the best (w, b) in that space
    Pa = np.hstack([P, np.ones((len(P), 1))])
    s3 = smo(Pa @ Pa.T, y, C=1e6, tol=1e-8)
    w3 = (s3["alpha"] * t) @ Pa
    gam = float(np.min(t * (Pa @ w3)) / np.linalg.norm(w3))
    R = float(np.linalg.norm(Pa, axis=1).max())
    out.update(perc_mistakes=mk, perc_bound=float((R / gam) ** 2), perc_w=wv)
    # the pages, two rates, Gaussian kernel: regions over C (gamma = 1) and the support vectors
    X, yy, test, X2 = split()
    Z2tr, Z2te, mu, sd = standardize(X2[~test], X2[test])
    ytr = yy[~test]
    xs, ys, G = grid2(X2)
    Gz = (G - mu) / sd
    out.update(xs=xs, ys=ys, mu=mu, sd=sd, Cs=SVM_CS, gammas=SVM_GS)
    Ktr = rbf(Z2tr, Z2tr, 1.0)
    Kte = rbf(Z2te, Z2tr, 1.0)
    Kg = rbf(Gz, Z2tr, 1.0)
    tt = 2.0 * ytr - 1
    for C in SVM_CS:
        s = smo(Ktr, ytr, C)
        prim, f = svm_primal(Ktr, ytr, s["alpha"], s["b"], C)
        key = f"C{C:g}"
        out[key] = dict(n_sv=len(s["sv"]), n_free=len(s["free"]), dual=s["dual"], primal=prim,
                        gap=float((prim - s["dual"]) / max(abs(prim), 1e-12)), iters=s["iters"],
                        train=acc_of(f, ytr, 0.0), test=acc_of(Kte @ (s["alpha"] * tt) + s["b"], yy[test], 0.0),
                        at_bound=int((s["alpha"] > C - 1e-8).sum()), viol=s["gap_viol"])
        out[f"region_{key}"] = (Kg @ (s["alpha"] * tt) + s["b"]).reshape(len(ys), len(xs))
        out[f"sv_{key}"] = s["sv"]
        out[f"alpha_{key}"] = s["alpha"]
        if C == 1.0:
            # KKT, checked point by point: a = 0 outside the street, 0 < a < C on its edge, a = C inside it
            m_ = tt * f
            out["kkt"] = dict(outside=int(((s["alpha"] < 1e-8) & (m_ < 1 - 1e-3)).sum()),
                              free_off=float(np.abs(m_[s["free"]] - 1).max()) if len(s["free"]) else 0.0,
                              bound_out=int(((s["alpha"] > C - 1e-8) & (m_ > 1 + 1e-3)).sum()))
    # regions over gamma (C = 1)
    for gm in SVM_GS:
        Kt = rbf(Z2tr, Z2tr, gm)
        s = smo(Kt, ytr, 1.0)
        out[f"region_g{gm:g}"] = (rbf(Gz, Z2tr, gm) @ (s["alpha"] * tt) + s["b"]).reshape(len(ys), len(xs))
        out[f"g{gm:g}"] = dict(n_sv=len(s["sv"]), test=acc_of(rbf(Z2te, Z2tr, gm) @ (s["alpha"] * tt) + s["b"], yy[test], 0.0))
    # cross-validated accuracy over (C, gamma), ten folds of the training pages
    f = kfold(ytr, seed=1995)
    cv = np.zeros((len(SVM_CS), len(SVM_GS), FOLDS))
    for k in range(FOLDS):
        a, b, _, _ = standardize(X2[~test][f != k], X2[~test][f == k])
        for j, gm in enumerate(SVM_GS):
            Ka, Kb = rbf(a, a, gm), rbf(b, a, gm)
            for i, C in enumerate(SVM_CS):
                s = smo(Ka, ytr[f != k], C, tol=1e-3)
                cv[i, j, k] = acc_of(Kb @ (s["alpha"] * (2.0 * ytr[f != k] - 1)) + s["b"], ytr[f == k], 0.0)
    cm = cv.mean(2)
    i, j = np.unravel_index(int(np.argmax(cm)), cm.shape)
    out.update(cv=cm, cv_sd=cv.std(2, ddof=1), C_cv=SVM_CS[i], g_cv=SVM_GS[j])
    s = smo(rbf(Z2tr, Z2tr, SVM_GS[j]), ytr, SVM_CS[i])
    out["acc_cv2"] = acc_of(rbf(Z2te, Z2tr, SVM_GS[j]) @ (s["alpha"] * tt) + s["b"], yy[test], 0.0)
    # all 70 rates: linear and Gaussian (gamma = 1/70) at C = 1
    Ztr, Zte, _, _ = standardize(X[~test], X[test])
    s = smo(Ztr @ Ztr.T, ytr, 1.0)
    out["acc70_lin"] = acc_of(Zte @ Ztr.T @ (s["alpha"] * tt) + s["b"], yy[test], 0.0)
    out["n_sv70_lin"] = len(s["sv"])
    s = smo(rbf(Ztr, Ztr, 1 / 70), ytr, 1.0)
    out["acc70_rbf"] = acc_of(rbf(Zte, Ztr, 1 / 70) @ (s["alpha"] * tt) + s["b"], yy[test], 0.0)
    out["n_sv70_rbf"] = len(s["sv"])
    out["n_train"] = int(len(ytr))
    return out


# ---------------------------------------------------------------------------
class Tree:
    """CART: classification (Gini) or regression (squared error) trees, grown greedily."""

    def __init__(self, depth=None, min_leaf=1, max_features=None, regression=False, seed=0):
        self.depth, self.min_leaf, self.mf, self.reg = depth, min_leaf, max_features, regression
        self.g = rng(seed)

    def fit(self, X, y, w=None):
        self.root = self._grow(X, y, 0)
        return self

    def _leaf(self, y):
        return {"leaf": float(y.mean())}

    def _grow(self, X, y, d):
        n = len(y)
        if (self.depth is not None and d >= self.depth) or n < 2 * self.min_leaf or np.all(y == y[0]):
            return self._leaf(y)
        feats = np.arange(X.shape[1])
        if self.mf:
            feats = self.g.choice(feats, size=self.mf, replace=False)
        best = (0.0, None, None)
        base = n * y.var() if self.reg else n * 2 * y.mean() * (1 - y.mean())
        for j in feats:
            o = np.argsort(X[:, j], kind="stable")
            xs, ys = X[o, j], y[o]
            cs, cs2 = np.cumsum(ys), np.cumsum(ys * ys)
            k = np.arange(1, n)
            ok = (xs[1:] > xs[:-1]) & (k >= self.min_leaf) & (n - k >= self.min_leaf)
            if not ok.any():
                continue
            sl, sr = cs[:-1], cs[-1] - cs[:-1]
            if self.reg:
                ql, qr = cs2[:-1], cs2[-1] - cs2[:-1]
                cost = (ql - sl ** 2 / k) + (qr - sr ** 2 / (n - k))
            else:
                pl, pr = sl / k, sr / (n - k)
                cost = k * 2 * pl * (1 - pl) + (n - k) * 2 * pr * (1 - pr)
            cost = np.where(ok, cost, np.inf)
            i = int(np.argmin(cost))
            gain = base - cost[i]
            if gain > best[0] + 1e-12:
                best = (gain, j, 0.5 * (xs[i] + xs[i + 1]))
        if best[1] is None:
            return self._leaf(y)
        j, t = best[1], best[2]
        m = X[:, j] <= t
        return {"j": int(j), "t": float(t), "l": self._grow(X[m], y[m], d + 1), "r": self._grow(X[~m], y[~m], d + 1)}

    def predict(self, X):
        out = np.empty(len(X))
        for i, x in enumerate(X):
            nd = self.root
            while "leaf" not in nd:
                nd = nd["l"] if x[nd["j"]] <= nd["t"] else nd["r"]
            out[i] = nd["leaf"]
        return out


def leaves(node, box, out):
    """The rectangles of a tree on two features: (x0, x1, y0, y1, value)."""
    if "leaf" in node:
        out.append([*box, node["leaf"]])
        return out
    x0, x1, y0, y1 = box
    if node["j"] == 0:
        leaves(node["l"], [x0, min(x1, node["t"]), y0, y1], out)
        leaves(node["r"], [max(x0, node["t"]), x1, y0, y1], out)
    else:
        leaves(node["l"], [x0, x1, y0, min(y1, node["t"])], out)
        leaves(node["r"], [x0, x1, max(y0, node["t"]), y1], out)
    return out


def impurity(p, kind):
    p = np.clip(p, 1e-12, 1 - 1e-12)
    if kind == "gini":
        return 2 * p * (1 - p)
    if kind == "entropy":
        return -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    return np.minimum(p, 1 - p)


def compute_trees():
    X, y, test, X2 = split()
    xs, ys, _ = grid2(X2)
    box = [float(xs[0]), float(xs[-1]), float(ys[0]), float(ys[-1])]
    out = dict(box=box, depths=list(range(1, 7)))
    for d in range(1, 7):
        t = Tree(depth=d, min_leaf=3).fit(X2[~test], y[~test])
        out[f"rects{d}"] = leaves(t.root, box, [])
        out[f"acc{d}"] = acc_of(t.predict(X2[test]), y[test])
        out[f"train{d}"] = acc_of(t.predict(X2[~test]), y[~test])
    out["tree3"] = Tree(depth=3, min_leaf=3).fit(X2[~test], y[~test]).root  # the tree itself, for its diagram
    deep = Tree(min_leaf=1).fit(X2[~test], y[~test])
    out["acc_deep2"] = acc_of(deep.predict(X2[test]), y[test])
    out["train_deep2"] = acc_of(deep.predict(X2[~test]), y[~test])
    out["rects_deep"] = leaves(deep.root, box, [])
    one = Tree(min_leaf=1).fit(X[~test], y[~test])
    out["acc_tree70"] = acc_of(one.predict(X[test]), y[test])
    # the root question, scanned: the impurity left after every threshold on "not" and on "the"
    ytr = y[~test].astype(float)
    n = len(ytr)
    for j, nm in ((1, "not"), (0, "the")):
        o = np.argsort(X2[~test][:, j], kind="stable")
        xv, yv = X2[~test][o, j], ytr[o]
        k = np.arange(1, n)
        ok = xv[1:] > xv[:-1]
        cs = np.cumsum(yv)[:-1]
        pl, pr = cs / k, (yv.sum() - cs) / (n - k)
        thr = 0.5 * (xv[1:] + xv[:-1])[ok]
        out[f"scan_{nm}_t"] = thr
        for kind in ("gini", "entropy", "error"):
            base = impurity(ytr.mean(), kind)
            after = (k * impurity(pl, kind) + (n - k) * impurity(pr, kind)) / n
            out[f"scan_{nm}_{kind}"] = (base - after)[ok]
    # cross-validated accuracy against depth, ten folds of the training pages
    f = kfold(y[~test], seed=1984)
    cv = np.zeros((FOLDS, 7))
    for kf in range(FOLDS):
        a, b = X2[~test][f != kf], X2[~test][f == kf]
        for i, d in enumerate([1, 2, 3, 4, 5, 6, None]):
            cv[kf, i] = acc_of(Tree(depth=d, min_leaf=3 if d else 1).fit(a, y[~test][f != kf]).predict(b), y[~test][f == kf])
    out["cv"], out["cv_sd"] = cv.mean(0), cv.std(0, ddof=1)
    return out


# ---------------------------------------------------------------------------
def compute_bagging():
    """(1) The formula, checked on equicorrelated Gaussians.  (2) On the pages: trees grown on many training sets,
    (150 pages each, drawn from the 448), their spread sigma^2 and correlation rho measured at the test pages, and the spread of an average of B of them
    against rho sigma^2 + (1 - rho) sigma^2 / B; for bagging (all 70 words at every question) and random forests
    (8 words, or 2).  (3) A forest of 300 on all training pages: test and out-of-bag accuracy as it grows."""
    out = {}
    g = rng(1996)  # Breiman, Bagging Predictors, 1996
    Bs = [1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 100]
    syn = {}
    for rho in (0.0, 0.2, 0.5, 0.8):
        R = 20000
        Z0 = g.standard_normal(R)
        Zb = g.standard_normal((R, Bs[-1]))
        V = math.sqrt(rho) * Z0[:, None] + math.sqrt(1 - rho) * Zb
        cm = np.cumsum(V, 1)
        syn[str(rho)] = [float((cm[:, B - 1] / B).var()) for B in Bs]
    out.update(syn=syn, syn_B=Bs)
    X, y, test, _ = split()
    Xtr, ytr, Xte, yte = X[~test], y[~test], X[test], y[test]
    Rs, T, m = 30, 50, 150
    params = dict(Rs=Rs, T=T, m=m)
    part = CACHE.partial("bagging", params)
    Bm = [1, 2, 3, 5, 10, 20, 30, 50]
    for mf in (70, 8, 2):
        key = f"mf{mf}"
        if key not in part:
            gg = rng(2001 + mf)
            preds = np.zeros((Rs, T, len(yte)))
            for r in range(Rs):
                sub = gg.integers(0, len(ytr), m)  # a fresh training set: 150 pages drawn from the 448
                for k in range(T):
                    bs = sub[gg.integers(0, len(sub), len(sub))]  # its bootstrap resample
                    tr = Tree(min_leaf=1, max_features=None if mf == 70 else mf, seed=int(gg.integers(1 << 30)))
                    preds[r, k] = tr.fit(Xtr[bs], ytr[bs]).predict(Xte)
            s2 = preds.reshape(-1, len(yte)).var(0)  # one tree's variance, over training sets and resamples
            cov = (preds.mean(1).var(0) * T - s2) / (T - 1)  # between-tree covariance: Var(mean of T) = cov + (s2 - cov)/T
            meas = []
            for B in Bm:
                meas.append(float(preds[:, :B].mean(1).var(0).mean()))
            acc = [float(np.mean([acc_of(preds[r, :B].mean(0), yte) for r in range(Rs)])) for B in Bm]
            part[key] = dict(s2=float(s2.mean()), cov=float(cov.mean()), rho=float(cov.mean() / s2.mean()),
                             meas=meas, acc=acc)
            print(f"    max_features {mf}: rho {part[key]['rho']:.3f}, sigma^2 {part[key]['s2']:.3f}", flush=True)
        out[key] = part[key]
    out.update(Bm=Bm, Rs=Rs, T=T, m=m)
    # one forest on all the training pages: accuracy and out-of-bag accuracy as it grows
    gg = rng(2001)
    nT = 300
    votes, oob_votes, oob_cnt = np.zeros(len(yte)), np.zeros(len(ytr)), np.zeros(len(ytr))
    f_acc, f_oob, b_acc = [], [], []
    bag_votes = np.zeros(len(yte))
    for k in range(nT):
        bs = gg.integers(0, len(ytr), len(ytr))
        t = Tree(min_leaf=1, max_features=8, seed=k).fit(Xtr[bs], ytr[bs])
        votes += t.predict(Xte)
        oob = np.setdiff1d(np.arange(len(ytr)), bs)
        oob_votes[oob] += t.predict(Xtr[oob])
        oob_cnt[oob] += 1
        f_acc.append(acc_of(votes / (k + 1), yte))
        seen = oob_cnt > 0
        f_oob.append(float(((oob_votes[seen] / oob_cnt[seen] > 0.5) == ytr[seen]).mean()))
        if k < 100:
            bs2 = gg.integers(0, len(ytr), len(ytr))
            bag_votes += Tree(min_leaf=1).fit(Xtr[bs2], ytr[bs2]).predict(Xte)
            b_acc.append(acc_of(bag_votes / (k + 1), yte))
    out.update(forest_acc=f_acc, forest_oob=f_oob, bag_acc=b_acc,
               one_tree=acc_of(Tree(min_leaf=1).fit(Xtr, ytr).predict(Xte), yte))
    part.finish()
    return out


# ---------------------------------------------------------------------------
def stumps_fit(X, t, w, order):
    """The best weighted stump: feature, threshold, polarity (+1: above the threshold says t = +1)."""
    n, d = X.shape
    best = (np.inf, 0, 0.0, 1)
    pos = np.where(t > 0, w, 0.0)
    neg = np.where(t < 0, w, 0.0)
    Wp, Wn = pos.sum(), neg.sum()
    for j in range(d):
        o = order[:, j]
        xs = X[o, j]
        cp, cn = np.cumsum(pos[o]), np.cumsum(neg[o])
        ok = np.r_[xs[1:] > xs[:-1], False]
        # polarity +1: left says -1 (errors: positives on the left), right says +1 (errors: negatives on the right)
        e1 = cp + (Wn - cn)
        e2 = cn + (Wp - cp)
        e1 = np.where(ok, e1, np.inf)
        e2 = np.where(ok, e2, np.inf)
        i1, i2 = int(np.argmin(e1)), int(np.argmin(e2))
        for e, i, pol in ((e1[i1], i1, 1), (e2[i2], i2, -1)):
            if e < best[0]:
                best = (float(e), j, float(0.5 * (xs[i] + xs[min(i + 1, n - 1)])), pol)
    return best


def stump_predict(X, j, thr, pol):
    return np.where(X[:, j] > thr, pol, -pol).astype(float)


AB_SNAPS = [1, 2, 3, 5, 10, 30, 100, 300]


def compute_adaboost():
    out = {}
    X, y, test, X2 = split()
    for name, A_tr, A_te, T in (("70", X[~test], X[test], 400), ("2", X2[~test], X2[test], 300)):
        t = 2.0 * y[~test] - 1
        te = 2.0 * y[test] - 1
        n = len(t)
        order = np.argsort(A_tr, 0, kind="stable")
        w = np.full(n, 1 / n)
        F, Fte = np.zeros(n), np.zeros(len(te))
        rec = dict(eps=[], alpha=[], exp_loss=[], train_err=[], test_err=[], stumps=[])
        if name == "2":
            xs, ys, G = grid2(X2)
            Fg = np.zeros(len(G))
            out.update(xs=xs, ys=ys)
        for k in range(1, T + 1):
            e, j, thr, pol = stumps_fit(A_tr, t, w, order)
            eps = e / w.sum()
            alpha = 0.5 * math.log((1 - eps) / eps)
            h = stump_predict(A_tr, j, thr, pol)
            if k <= 5 and name == "70":
                # alpha by brute force: minimize the exponential loss along this stump
                grid = np.linspace(0, 3, 30001)
                L = [np.mean(np.exp(-t * (F + a * h))) for a in grid[::30]]
                a0 = grid[::30][int(np.argmin(L))]
                fine = np.linspace(max(a0 - 0.01, 0), a0 + 0.01, 2001)
                Lf = [np.mean(np.exp(-t * (F + a * h))) for a in fine]
                rec.setdefault("alpha_search", []).append(float(fine[int(np.argmin(Lf))]))
            F += alpha * h
            Fte += alpha * stump_predict(A_te, j, thr, pol)
            w = np.exp(-t * F)
            w /= w.sum()
            rec["eps"].append(float(eps))
            rec["alpha"].append(float(alpha))
            rec["exp_loss"].append(float(np.mean(np.exp(-t * F))))
            rec["train_err"].append(float(np.mean(np.sign(F) != t)))
            rec["test_err"].append(float(np.mean(np.sign(Fte) != te)))
            rec["stumps"].append([int(j), float(thr), int(pol)])
            if name == "2":
                Fg += alpha * stump_predict(G, j, thr, pol)
                if k in AB_SNAPS:
                    out[f"region{k}"] = np.tanh(Fg).reshape(len(ys), len(xs))
                    out[f"w{k}"] = w.copy()
        for kk, v in rec.items():
            out[f"{kk}_{name}"] = v
    a = np.array(out["alpha_70"][:5])
    s = np.array(out["alpha_search_70"])
    out["alpha_check"] = float(np.abs(a - s).max())
    out["snaps"] = AB_SNAPS
    p = load("pages")
    out["first_words"] = [p["vocab"][j] for j, _, _ in out["stumps_70"][:6]]
    # the bound: training error <= exponential loss, every round
    assert all(e <= l_ + 1e-12 for e, l_ in zip(out["train_err_70"], out["exp_loss_70"]))
    return out


# ---------------------------------------------------------------------------
class XTree:
    """A regression tree grown by XGBoost's rule: leaf weight -G/(H + lam), split gain
    1/2 [G_L^2/(H_L+lam) + G_R^2/(H_R+lam) - (G_L+G_R)^2/(H_L+H_R+lam)] - gamma."""

    def __init__(self, depth=3, lam=1.0, gamma=0.0, min_child=1.0):
        self.depth, self.lam, self.gamma, self.mc = depth, lam, gamma, min_child

    def fit(self, X, g, h):
        self.root = self._grow(X, g, h, 0)
        return self

    def best_split(self, X, g, h):
        G, H, lam = g.sum(), h.sum(), self.lam
        best = (0.0, None, None)
        for j in range(X.shape[1]):
            o = np.argsort(X[:, j], kind="stable")
            xs = X[o, j]
            GL, HL = np.cumsum(g[o])[:-1], np.cumsum(h[o])[:-1]
            GR, HR = G - GL, H - HL
            ok = (xs[1:] > xs[:-1]) & (HL >= self.mc) & (HR >= self.mc)
            if not ok.any():
                continue
            gain = 0.5 * (GL ** 2 / (HL + lam) + GR ** 2 / (HR + lam) - G ** 2 / (H + lam)) - self.gamma
            gain = np.where(ok, gain, -np.inf)
            i = int(np.argmax(gain))
            if gain[i] > best[0]:
                best = (float(gain[i]), j, float(0.5 * (xs[i] + xs[i + 1])))
        return best

    def _grow(self, X, g, h, d):
        leaf = {"leaf": float(-g.sum() / (h.sum() + self.lam))}
        if d >= self.depth or len(g) < 2:
            return leaf
        gain, j, t = self.best_split(X, g, h)
        if j is None:
            return leaf
        m = X[:, j] <= t
        return {"j": j, "t": t, "gain": gain, "l": self._grow(X[m], g[m], h[m], d + 1),
                "r": self._grow(X[~m], g[~m], h[~m], d + 1)}

    def predict(self, X):
        out = np.empty(len(X))
        for i, x in enumerate(X):
            nd = self.root
            while "leaf" not in nd:
                nd = nd["l"] if x[nd["j"]] <= nd["t"] else nd["r"]
            out[i] = nd["leaf"]
        return out


XGB_SNAPS = [1, 3, 10, 30, 100, 200]


def compute_xgb():
    X, y, test, X2 = split()
    out = {}
    lam, eta, depth, T = 1.0, 0.3, 3, 200
    # the gain formula, checked on the first split: the second-order objective evaluated leaf by leaf, directly
    ytr = y[~test].astype(float)
    p = np.full(len(ytr), 0.5)
    g, h = p - ytr, p * (1 - p)
    tr = XTree(depth=1, lam=lam)
    gain, j, thr = tr.best_split(X[~test], g, h)
    m = X[~test][:, j] <= thr

    def obj(mask):  # min over one leaf weight of sum(g w + h w^2 / 2) + lam w^2 / 2
        G, H = g[mask].sum(), h[mask].sum()
        w = -G / (H + lam)
        return float(G * w + 0.5 * (H + lam) * w * w)

    direct = obj(np.ones(len(g), bool)) - obj(m) - obj(~m)
    # and the true drop in log loss from that one split (a full step), against the second-order prediction
    wl, wr = -g[m].sum() / (h[m].sum() + lam), -g[~m].sum() / (h[~m].sum() + lam)
    F1 = np.where(m, wl, wr)
    w0 = -g.sum() / (h.sum() + lam)
    true_drop = (logloss(np.full(len(ytr), w0), ytr) - logloss(F1, ytr)) * len(ytr)
    p_ = load("pages")
    out.update(check_gain=gain, check_direct=direct, check_true=float(true_drop), check_word=p_["vocab"][j],
               check_thr=thr, check_G=[float(g[m].sum()), float(g[~m].sum())], check_H=[float(h[m].sum()), float(h[~m].sum())])
    assert abs(gain - direct) < 1e-9 * max(1, abs(gain))
    for name, A_tr, A_te in (("70", X[~test], X[test]), ("2", X2[~test], X2[test])):
        F, Fte = np.zeros(len(ytr)), np.zeros(int(test.sum()))
        F1o, F1te = np.zeros(len(ytr)), np.zeros(int(test.sum()))  # first order: leaves = mean negative gradient
        rec = dict(train_loss=[], test_loss=[], test_acc=[], train_acc=[], first_loss=[], first_acc=[])
        if name == "2":
            xs, ys, G = grid2(X2)
            Fg = np.zeros(len(G))
            out.update(xs=xs, ys=ys)
        for k in range(1, T + 1):
            pp = sigmoid(F)
            t_ = XTree(depth=depth, lam=lam).fit(A_tr, pp - ytr, pp * (1 - pp))
            F += eta * t_.predict(A_tr)
            Fte += eta * t_.predict(A_te)
            p1 = sigmoid(F1o)
            t1 = Tree(depth=depth, regression=True).fit(A_tr, ytr - p1)
            F1o += eta * t1.predict(A_tr)
            F1te += eta * t1.predict(A_te)
            rec["train_loss"].append(logloss(F, ytr) / math.log(2))
            rec["test_loss"].append(logloss(Fte, y[test]) / math.log(2))
            rec["test_acc"].append(acc_of(Fte, y[test], 0.0))
            rec["train_acc"].append(acc_of(F, ytr, 0.0))
            rec["first_loss"].append(logloss(F1o, ytr) / math.log(2))
            rec["first_acc"].append(acc_of(F1te, y[test], 0.0))
            if name == "2":
                Fg += eta * t_.predict(G)
                if k in XGB_SNAPS:
                    out[f"region{k}"] = sigmoid(Fg).reshape(len(ys), len(xs))
        for kk, v in rec.items():
            out[f"{kk}_{name}"] = v
    out.update(snaps=XGB_SNAPS, lam=lam, eta=eta, depth=depth, T=T)
    return out


# ---------------------------------------------------------------------------
def roc(scores, y):
    """ROC and precision-recall points at every distinct threshold (tied scores move together)."""
    scores = np.asarray(scores, float)
    o = np.argsort(-scores, kind="stable")
    ys, ss = y[o], scores[o]
    last = np.r_[ss[1:] != ss[:-1], True]  # the end of each run of tied scores
    tp, fp = np.cumsum(ys)[last], np.cumsum(1 - ys)[last]
    P, N = ys.sum(), (1 - ys).sum()
    tpr, fpr = np.r_[0, tp / P], np.r_[0, fp / N]
    prec = tp / (tp + fp)
    rec = tp / P
    auc = float(np.trapezoid(tpr, fpr))
    ap = float(np.sum(np.diff(np.r_[0, rec]) * prec))  # average precision: precision, weighted by recall gained
    return tpr, fpr, prec, rec, auc, ap


def mann_whitney(scores, y):
    a, d = scores[y == 0], scores[y == 1]
    gt = (d[:, None] > a[None]).sum() + 0.5 * (d[:, None] == a[None]).sum()
    return float(gt / (len(a) * len(d)))


def compute_metrics():
    out = {}
    cal = load("calibration")
    _, y, _, _ = split()
    for k in ("lr2", "lr70", "nb"):
        s = np.asarray(cal[f"p_{k}"]) if k != "nb" else np.asarray(cal["nb_z"])
        tpr, fpr, prec, rec, auc, ap = roc(s, y)
        out[k] = dict(auc=auc, ap=ap, mw=mann_whitney(s, y))
        step = max(1, len(tpr) // 160)
        out[f"roc_{k}"] = np.stack([fpr[::step], tpr[::step]], 1)
        out[f"pr_{k}"] = np.stack([rec[::step], prec[::step]], 1)
        assert abs(auc - out[k]["mw"]) < 1e-9
    # rare Dickens: keep every Austen page and 5% as many Dickens pages; many draws
    g = rng(2006)
    s2 = np.asarray(cal["p_lr2"])
    A, D = np.nonzero(y == 0)[0], np.nonzero(y == 1)[0]
    aucs, aps, base = [], [], []
    nd = int(round(0.05 / 0.95 * len(A)))
    for _ in range(200):
        idx = np.r_[A, g.choice(D, nd, replace=False)]
        _, _, _, _, a_, p_ = roc(s2[idx], y[idx])
        aucs.append(a_)
        aps.append(p_)
    tpr, fpr, prec, rec, _, _ = roc(s2[idx], y[idx])
    out["rare"] = dict(n_dickens=nd, n_austen=len(A), auc=float(np.mean(aucs)), auc_lo=float(np.percentile(aucs, 10)),
                       auc_hi=float(np.percentile(aucs, 90)), ap=float(np.mean(aps)), ap_lo=float(np.percentile(aps, 10)),
                       ap_hi=float(np.percentile(aps, 90)), always_austen=float(len(A) / (len(A) + nd)))
    out["roc_rare"] = np.stack([fpr, tpr], 1)
    out["pr_rare"] = np.stack([rec, prec], 1)
    # how much does one estimate of accuracy wobble?  logistic regression on two rates
    X, y, test, X2 = split()
    split_acc = []
    for s in range(100):  # 100 different random 70/30 splits
        gg = rng(3000 + s)
        te = np.zeros(len(y), bool)
        for lab in (0, 1):
            idx = np.nonzero(y == lab)[0]
            te[gg.choice(idx, int(round(0.3 * len(idx))), replace=False)] = True
        a, b, _, _ = standardize(X2[~te], X2[te])
        w, c = newton_logreg(a, y[~te].astype(float), l2=0.0)
        split_acc.append(acc_of(b @ w + c, y[te], 0.0))
    cv_acc = []
    fold_acc = []
    for rep in range(20):  # ten-fold cross-validation, repeated with 20 shufflings
        f = kfold(y, seed=4000 + rep)
        hits = np.zeros(len(y))
        for k in range(FOLDS):
            a, b, _, _ = standardize(X2[f != k], X2[f == k])
            w, c = newton_logreg(a, y[f != k].astype(float), l2=0.0)
            pr = (b @ w + c > 0) == y[f == k]
            hits[f == k] = pr
            fold_acc.append(float(pr.mean()))
        cv_acc.append(float(hits.mean()))
    out.update(split_acc=split_acc, cv_acc=cv_acc, fold_acc=fold_acc)
    return out


# ---------------------------------------------------------------------------
def methods():
    """Every method of the part, with the settings fixed in advance (no tuning on held-out pages).  Each takes
    (training features, training labels, test features) and returns scores (Dickens if above the threshold)."""

    def ls(a, ya, b, lam=0.0):
        A_, B_, _, _ = standardize(a, b)
        m = ya.mean()
        w = ridge_svd(A_, ya - m, lam)
        return B_ @ w + m

    def lasso(a, ya, b):
        A_, B_, _, _ = standardize(a, b)
        m = ya.mean()
        lam = 0.01 * float(np.abs(A_.T @ (ya - m)).max() / len(ya))
        w, _ = enet_cd(A_, ya - m, lam, tol=1e-7)
        return B_ @ w + m

    def lr(a, ya, b):
        A_, B_, _, _ = standardize(a, b)
        w, c = newton_logreg(A_, ya.astype(float), l2=1e-2)
        return sigmoid(B_ @ w + c)

    def nb(a, ya, b):
        w, c = nb_fit(a, ya)
        return sigmoid(b @ w + c)

    def lda(a, ya, b):
        A_, B_, _, _ = standardize(a, b)
        ZA, ZD = A_[ya == 0], A_[ya == 1]
        S = (np.cov(ZA.T) * (len(ZA) - 1) + np.cov(ZD.T) * (len(ZD) - 1)) / (len(A_) - 2)
        S = np.atleast_2d(S) + 1e-3 * np.eye(A_.shape[1])
        w = np.linalg.solve(S, ZD.mean(0) - ZA.mean(0))
        pi = ya.mean()
        c = float(w @ (ZA.mean(0) + ZD.mean(0)) / 2 - math.log(pi / (1 - pi)))
        return sigmoid(B_ @ w - c)

    def knn(a, ya, b):
        A_, B_, _, _ = standardize(a, b)
        return knn_scores(A_, ya, B_, 15)

    def svm_lin(a, ya, b):
        A_, B_, _, _ = standardize(a, b)
        s = smo(A_ @ A_.T, ya, 1.0, tol=1e-3)
        return B_ @ A_.T @ (s["alpha"] * (2.0 * ya - 1)) + s["b"]

    def svm_rbf(a, ya, b):
        A_, B_, _, _ = standardize(a, b)
        gm = 1.0 / A_.shape[1]
        s = smo(rbf(A_, A_, gm), ya, 1.0, tol=1e-3)
        return rbf(B_, A_, gm) @ (s["alpha"] * (2.0 * ya - 1)) + s["b"]

    def tree(a, ya, b):
        return Tree(depth=4, min_leaf=3).fit(a, ya).predict(b)

    def forest(a, ya, b, seed=0):
        g = rng(seed)
        mf = max(1, int(round(math.sqrt(a.shape[1]))))
        v = np.zeros(len(b))
        for k in range(200):
            bs = g.integers(0, len(ya), len(ya))
            v += Tree(min_leaf=1, max_features=mf if a.shape[1] > 2 else None, seed=int(g.integers(1 << 30))).fit(
                a[bs], ya[bs]).predict(b)
        return v / 200

    def ada(a, ya, b):
        t = 2.0 * ya - 1
        order = np.argsort(a, 0, kind="stable")
        w = np.full(len(t), 1 / len(t))
        F, Fb = np.zeros(len(t)), np.zeros(len(b))
        for _ in range(200):
            e, j, thr, pol = stumps_fit(a, t, w, order)
            eps = min(max(e / w.sum(), 1e-10), 1 - 1e-10)
            al = 0.5 * math.log((1 - eps) / eps)
            F += al * stump_predict(a, j, thr, pol)
            Fb += al * stump_predict(b, j, thr, pol)
            w = np.exp(-t * F)
            w /= w.sum()
        return Fb

    def xgb(a, ya, b):
        F, Fb = np.zeros(len(ya)), np.zeros(len(b))
        for _ in range(100):
            pp = sigmoid(F)
            t_ = XTree(depth=3, lam=1.0).fit(a, pp - ya, pp * (1 - pp))
            F += 0.3 * t_.predict(a)
            Fb += 0.3 * t_.predict(b)
        return Fb

    return [
        ("ls", "least squares", ls, 0.5, (2, 70)),
        ("lasso", "lasso", lasso, 0.5, (70,)),
        ("lr", "logistic regression", lr, 0.5, (2, 70)),
        ("nb", "naive Bayes", nb, 0.5, (70,)),
        ("lda", "LDA (Fisher)", lda, 0.5, (2, 70)),
        ("knn", "15 nearest neighbours", knn, 0.5, (2, 70)),
        ("svm_lin", "linear SVM", svm_lin, 0.0, (2, 70)),
        ("svm_rbf", "Gaussian-kernel SVM", svm_rbf, 0.0, (2, 70)),
        ("tree", "one tree (depth 4)", tree, 0.5, (2, 70)),
        ("forest", "random forest (200)", forest, 0.5, (2, 70)),
        ("ada", "AdaBoost (200 stumps)", ada, 0.0, (2, 70)),
        ("xgb", "gradient boosting (100)", xgb, 0.0, (2, 70)),
    ]


def compute_board():
    """Every method on the same ten stratified folds of all 639 pages (mean and spread over folds), and on the
    held-out pages after training on the training pages; with the two plotted rates and with all 70."""
    X, y, test, X2 = split()
    f = kfold(y, seed=2025)
    params = dict(folds=FOLDS, seed=2025, v=1)
    part = CACHE.partial("board", params)
    rows = []
    for key, name, fn, thr, feats in methods():
        row = dict(key=key, name=name)
        for nf in (2, 70):
            if nf not in feats:
                continue
            k_ = f"{key}_{nf}"
            if k_ not in part:
                A = X2 if nf == 2 else X
                accs = [acc_of(fn(A[f != k], y[f != k], A[f == k]), y[f == k], thr) for k in range(FOLDS)]
                held = acc_of(fn(A[~test], y[~test], A[test]), y[test], thr)
                part[k_] = dict(cv=float(np.mean(accs)), sd=float(np.std(accs, ddof=1)), lo=float(min(accs)),
                                hi=float(max(accs)), folds=accs, held=held)
                print(f"    {name:28s} {nf:2d} rates: {part[k_]['cv']:.3f} +- {part[k_]['sd']:.3f}", flush=True)
            row[str(nf)] = part[k_]
        rows.append(row)
    part.finish()
    return dict(rows=rows, n=len(y), folds=FOLDS)


def _plain(v):
    """Nested arrays and numpy scalars as lists and floats (the top level's arrays go to the .npz as they are)."""
    if isinstance(v, dict):
        return {str(k): _plain(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    if isinstance(v, np.ndarray):
        return v.tolist()
    if isinstance(v, np.generic):
        return v.item()
    return v


def _item(fn):
    def run():
        return {k: (v if isinstance(v, np.ndarray) else _plain(v)) for k, v in fn().items()}

    run.__name__ = fn.__name__
    return run


ITEMS = {
    "pages": compute_pages,
    "zipf": compute_zipf,
    "gaussmarkov": compute_gaussmarkov,
    "lsq": compute_lsq,
    "ridge": compute_ridge,
    "lasso": compute_lasso,
    "logistic": compute_logistic,
    "irls": compute_irls,
    "calibration": compute_calibration,
    "nbvslr": compute_nbvslr,
    "lda": compute_lda,
    "knn": compute_knn,
    "coverhart": compute_coverhart,
    "curse": compute_curse,
    "kernel": compute_kernel,
    "svm": compute_svm,
    "trees": compute_trees,
    "bagging": compute_bagging,
    "adaboost": compute_adaboost,
    "xgb": compute_xgb,
    "metrics": compute_metrics,
    "board": compute_board,
}
ITEMS = {k: (v if k == "pages" else _item(v)) for k, v in ITEMS.items()}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
