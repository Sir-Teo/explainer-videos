"""Precompute everything numerical in Part 5 of the AI series ("Classical ML").

    python -m videos.ai.ai5.compute              # everything missing (Part 1's books are reused: .cache/ai1)
    python -m videos.ai.ai5.compute --force trees

Results are cached in ``.cache/ai5/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Every method is written
out here in numpy (no machine-learning library), and every number the narration quotes is computed here.

The task, for every method: who wrote this page, Jane Austen or Charles Dickens?  Pages are 1,000-word chunks of
five novels (Pride and Prejudice and Emma; A Tale of Two Cities, Great Expectations and A Christmas Carol); a page
is described by how often it uses the 70 commonest words (per 1,000 words), as Mosteller and Wallace described the
Federalist papers in 1964.  70% of the pages train, 30% are held out to test.  The pictures use two of the 70
numbers: how often a page says "the", and how often it says "not".

Items:
    pages      the pages, their 70 rates, labels, the train/test split, the two plotted rates, one test page's text
    zipf       least squares on Zipf's law: log frequency against log rank for the commonest 1,000 words of the books
    logistic   logistic regression on the two rates (the boundary, the probability sheet) and on all 70
    lasso      L1- and L2-penalized logistic regression on all 70 rates, along a path of penalties
    lda        Fisher's discriminant on the two rates: the separation along every direction, the best one
    knn        k nearest neighbours on the two rates, k = 1, 15, 75: regions and accuracy
    svm        support vector machines on the two rates: linear (margin, support vectors) and a Gaussian kernel
    trees      a decision tree on the two rates (depth 1 to 6); a random forest and gradient boosting on all 70
    board      the test accuracy of every method, on 2 rates and on 70
"""

from __future__ import annotations

import collections
import math
import re

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai5")
load = CACHE.load

AUSTEN = {1342: "Pride and Prejudice", 158: "Emma"}
DICKENS = {98: "A Tale of Two Cities", 1400: "Great Expectations", 46: "A Christmas Carol"}
PAGE = 1000  # words per page
N_WORDS = 70
PLOT = ("the", "not")  # the two rates in every picture
GRID = 120  # resolution of the decision-region pictures


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
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


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


def compute_logistic():
    X, y, test, X2 = split()
    Z2tr, Z2te, mu, sd = standardize(X2[~test], X2[test])
    w, b = logreg(Z2tr, y[~test], iters=4000)
    acc2 = float(((sigmoid(Z2te @ w + b) > 0.5) == y[test]).mean())
    Ztr, Zte, _, _ = standardize(X[~test], X[test])
    W, B = logreg(Ztr, y[~test], l2=1e-3, iters=4000)
    acc70 = float(((sigmoid(Zte @ W + B) > 0.5) == y[test]).mean())
    xs, ys, G = grid2(X2)
    prob = sigmoid(((G - mu) / sd) @ w + b).reshape(len(ys), len(xs))
    # the boundary in the original units: w . (x - mu) / sd + b = 0
    wr = w / sd
    b_raw = b - float(wr @ mu)
    loss = float(-np.mean(y[~test] * np.log(sigmoid(Z2tr @ w + b)) + (1 - y[~test]) * np.log(1 - sigmoid(Z2tr @ w + b))))
    assert acc70 > acc2 > 0.75
    # how it learns: the same gradient descent, its line (in the original units) and its loss along the way
    ytr = y[~test]
    n = len(ytr)
    lr = 1 / (0.25 * (np.linalg.norm(Z2tr, 2) ** 2 / n + 1))
    wt, bt = np.zeros(2), 0.0
    keep = {0, 1, 2, 3, 5, 8, 12, 20, 35, 60, 100, 180, 320, 600, 1200, 4000}
    path, curve = [], []
    for it in range(4001):
        pz = sigmoid(Z2tr @ wt + bt)
        ce = float(-np.mean(ytr * np.log(pz + 1e-12) + (1 - ytr) * np.log(1 - pz + 1e-12))) / math.log(2)
        curve.append((it, ce))
        if it in keep:
            path.append((it, *(wt / sd), bt - float((wt / sd) @ mu), ce))
        if it == 4000:
            break
        wt, bt = wt - lr * Z2tr.T @ (pz - ytr) / n, bt - lr * float((pz - ytr).mean())
    return dict(w=wr, b=b_raw, acc2=acc2, acc70=acc70, xs=xs, ys=ys, prob=prob, loss_bits=loss / math.log(2),
                path=np.array(path), curve=np.array(curve[::5] + [curve[-1]]))


# ---------------------------------------------------------------------------
def compute_lasso():
    p = load("pages")
    X, y, test, _ = split()
    vocab = p["vocab"]
    Ztr, Zte, _, _ = standardize(X[~test], X[test])
    ytr = y[~test]
    pbar = ytr.mean()
    lam_max = float(np.abs(Ztr.T @ (pbar - ytr)).max() / len(ytr))
    lams = lam_max * np.logspace(0, -2.2, 34)
    path, acc, ws = [], [], (np.zeros(Ztr.shape[1]), math.log(pbar / (1 - pbar)))
    for lam in lams:
        ws = logreg(Ztr, ytr, l1=lam, w0=ws, iters=1500)
        path.append(ws[0].copy())
        acc.append(float(((sigmoid(Zte @ ws[0] + ws[1]) > 0.5) == y[test]).mean()))
    path = np.array(path)
    order = []  # the order in which words get a nonzero weight
    for k in range(len(lams)):
        for i in np.nonzero(path[k])[0]:
            if vocab[i] not in order:
                order.append(vocab[i])
    rlams = np.logspace(1, -3, 30)
    rpath, ws = [], (np.zeros(Ztr.shape[1]), 0.0)
    for lam in rlams:
        ws = logreg(Ztr, ytr, l2=lam, w0=ws, iters=1500)
        rpath.append(ws[0].copy())
    k5 = int(np.argmax([np.count_nonzero(w) >= 5 for w in path]))
    assert np.count_nonzero(path[0]) <= 1 and np.count_nonzero(path[-1]) > 20
    return dict(lams=lams, path=path, acc=acc, order=order[:12], ridge_lams=rlams, ridge_path=np.array(rpath),
                k5=k5, acc5=acc[k5], words5=[vocab[i] for i in np.nonzero(path[k5])[0]])


# ---------------------------------------------------------------------------
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
    # the boundary: halfway between the projected means (equal priors)
    c = float(0.5 * ((A @ w).mean() + (D @ w).mean()))
    acc = float((((X2[test] @ w) > c) == y[test]).mean())
    return dict(w=w, c=c, angles=angles, sep=sep, best=best, acc2=acc, mA=A.mean(0), mD=D.mean(0),
                covA=np.cov(A.T), covD=np.cov(D.T))


# ---------------------------------------------------------------------------
def compute_knn():
    X, y, test, X2 = split()
    Z2tr, Z2te, mu, sd = standardize(X2[~test], X2[test])
    ytr = y[~test]
    xs, ys, G = grid2(X2)
    Gz = (G - mu) / sd
    out = dict(xs=xs, ys=ys, ks=[1, 15, 75])
    for k in (1, 15, 75):
        def predict(Q):
            d = ((Q[:, None, :] - Z2tr[None]) ** 2).sum(-1)
            nn = np.argpartition(d, k - 1, axis=1)[:, :k] if k > 1 else np.argmin(d, 1)[:, None]
            return ytr[nn].mean(1)
        out[f"acc{k}"] = float(((predict(Z2te) > 0.5) == y[test]).mean())
        out[f"train{k}"] = float(((predict(Z2tr) > 0.5) == ytr).mean())
        out[f"region{k}"] = predict(Gz).reshape(len(ys), len(xs))
    assert out["train1"] > 0.9 and out["acc15"] > out["acc1"] + 0.1
    return out


# ---------------------------------------------------------------------------
def svm_dual(K, y, C, epochs=300, seed=0):
    """Dual coordinate descent for the soft-margin SVM, max sum(a) - 1/2 a'Qa with 0 <= a <= C (the bias folded into
    the kernel as + 1).  Returns the alphas."""
    s = 2 * y - 1.0
    Q = K * s[:, None] * s[None]
    a = np.zeros(len(y))
    g = rng(seed)
    for _ in range(epochs):
        for i in g.permutation(len(y)):
            grad = Q[i] @ a - 1
            a[i] = min(max(a[i] - grad / Q[i, i], 0.0), C)
    return a


def compute_svm():
    X, y, test, X2 = split()
    Z2tr, Z2te, mu, sd = standardize(X2[~test], X2[test])
    ytr = y[~test]
    s = 2 * ytr - 1.0
    xs, ys, G = grid2(X2)
    Gz = (G - mu) / sd
    # linear: K = x.x' + 1
    C = 1.0
    a = svm_dual(Z2tr @ Z2tr.T + 1, ytr, C)
    w = (a * s) @ Z2tr
    b = float((a * s).sum())
    margin = 1 / np.linalg.norm(w)
    f_te = Z2te @ w + b
    sv = np.nonzero(a > 1e-6)[0]
    on = np.nonzero((a > 1e-6) & (a < C - 1e-6))[0]  # exactly on the margin
    acc_lin = float(((f_te > 0) == y[test]).mean())
    # Gaussian kernel
    gamma, C2 = 1.0, 3.0

    def rbf(P, Q):
        return np.exp(-gamma * ((P[:, None, :] - Q[None]) ** 2).sum(-1)) + 1

    a2 = svm_dual(rbf(Z2tr, Z2tr), ytr, C2, epochs=400)
    acc_rbf = float((((a2 * s) @ rbf(Z2tr, Z2te) > 0) == y[test]).mean())
    region = ((a2 * s) @ rbf(Z2tr, Gz)).reshape(len(ys), len(xs))
    # all 70 rates, Gaussian kernel (gamma scaled to the dimension)
    Ztr, Zte, _, _ = standardize(X[~test], X[test])
    g70 = 1.0 / Ztr.shape[1]
    K70 = np.exp(-g70 * ((Ztr[:, None] - Ztr[None]) ** 2).sum(-1)) + 1
    a70 = svm_dual(K70, ytr, 3.0, epochs=300)
    Kte = np.exp(-g70 * ((Ztr[:, None] - Zte[None]) ** 2).sum(-1)) + 1
    acc70 = float((((a70 * s) @ Kte > 0) == y[test]).mean())
    # back to the plotted units: the line w.(x - mu)/sd + b = 0, and the margins at +-1
    return dict(w=w / sd, b=b - float((w / sd) @ mu), margin_z=float(margin), sv=sv, on_margin=on, acc_lin=acc_lin,
                acc_rbf=acc_rbf, acc70=acc70, xs=xs, ys=ys, region=region, mu=mu, sd=sd, n_sv=len(sv))


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
            o = np.argsort(X[:, j])
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


def compute_trees():
    X, y, test, X2 = split()
    xs, ys, _ = grid2(X2)
    box = [float(xs[0]), float(xs[-1]), float(ys[0]), float(ys[-1])]
    out = dict(box=box, depths=list(range(1, 7)))
    for d in range(1, 7):
        t = Tree(depth=d, min_leaf=3).fit(X2[~test], y[~test])
        out[f"rects{d}"] = leaves(t.root, box, [])
        out[f"acc{d}"] = float(((t.predict(X2[test]) > 0.5) == y[test]).mean())
        out[f"train{d}"] = float(((t.predict(X2[~test]) > 0.5) == y[~test]).mean())
    out["tree3"] = Tree(depth=3, min_leaf=3).fit(X2[~test], y[~test]).root  # the tree itself, for its diagram
    deep = Tree(min_leaf=1).fit(X2[~test], y[~test])
    out["acc_deep2"] = float(((deep.predict(X2[test]) > 0.5) == y[test]).mean())
    out["train_deep2"] = float(((deep.predict(X2[~test]) > 0.5) == y[~test]).mean())
    out["rects_deep"] = leaves(deep.root, box, [])
    # all 70 rates: one deep tree, a forest of 200, gradient boosting
    Xtr, Xte, ytr = X[~test], X[test], y[~test]
    one = Tree(min_leaf=1).fit(Xtr, ytr)
    out["acc_tree70"] = float(((one.predict(Xte) > 0.5) == y[test]).mean())
    g = rng(2001)  # Breiman, Random Forests, 2001
    votes, forest_acc = np.zeros(len(Xte)), []
    for k in range(200):
        bs = g.integers(0, len(ytr), len(ytr))
        t = Tree(min_leaf=1, max_features=int(math.sqrt(X.shape[1])), seed=k).fit(Xtr[bs], ytr[bs])
        votes += t.predict(Xte)
        forest_acc.append(float(((votes / (k + 1) > 0.5) == y[test]).mean()))
    out["forest_acc"] = forest_acc
    # gradient boosting (logistic loss), depth-2 trees, learning rate 0.2
    F_tr, F_te = np.zeros(len(ytr)), np.zeros(len(Xte))
    boost_acc, boost_train = [], []
    for k in range(300):
        p = sigmoid(F_tr)
        t = Tree(depth=2, min_leaf=5, regression=True).fit(Xtr, ytr - p)
        F_tr += 0.2 * 4 * t.predict(Xtr)  # 4 = 1 / (p(1-p)) at p = 1/2, a one-step Newton scale
        F_te += 0.2 * 4 * t.predict(Xte)
        boost_acc.append(float(((F_te > 0) == y[test]).mean()))
        boost_train.append(float(((F_tr > 0) == ytr).mean()))
    out["boost_acc"], out["boost_train"] = boost_acc, boost_train
    assert out["train_deep2"] > 0.9 and forest_acc[-1] >= out["acc_tree70"], (out["train_deep2"], forest_acc[-1], out["acc_tree70"])
    return out


BOOST_SNAPS = (1, 3, 10, 30, 100, 300)


def compute_boost2():
    """Gradient boosting on the two plotted rates, as it learns: the committee's vote over the plane after 1, 3, 10,
    30, 100 and 300 rounds (the same recipe as the 70-rate boosting in `trees`), and its accuracy every round."""
    X, y, test, X2 = split()
    xs, ys, G = grid2(X2)
    Xtr, Xte, ytr = X2[~test], X2[test], y[~test]
    F_tr, F_te, F_g = np.zeros(len(ytr)), np.zeros(len(Xte)), np.zeros(len(G))
    out, acc, train = dict(xs=xs, ys=ys, snaps=list(BOOST_SNAPS)), [], []
    for k in range(1, BOOST_SNAPS[-1] + 1):
        t = Tree(depth=2, min_leaf=5, regression=True).fit(Xtr, ytr - sigmoid(F_tr))
        F_tr += 0.2 * 4 * t.predict(Xtr)
        F_te += 0.2 * 4 * t.predict(Xte)
        F_g += 0.2 * 4 * t.predict(G)
        acc.append(float(((F_te > 0) == y[test]).mean()))
        train.append(float(((F_tr > 0) == ytr).mean()))
        if k in BOOST_SNAPS:
            out[f"region{k}"] = sigmoid(F_g).reshape(len(ys), len(xs))
            print(f"    round {k}: train {train[-1]:.3f}, new pages {acc[-1]:.3f}", flush=True)
    out["acc"], out["train"] = np.array(acc), np.array(train)
    return out


# ---------------------------------------------------------------------------
def compute_board():
    lg, la, ld, kn, sv, tr = (load(k) for k in ("logistic", "lasso", "lda", "knn", "svm", "trees"))
    rows = [
        ("logistic regression", lg["acc2"], lg["acc70"]),
        ("LDA (Fisher)", ld["acc2"], None),
        ("15 nearest neighbours", kn["acc15"], None),
        ("SVM, linear", sv["acc_lin"], None),
        ("SVM, Gaussian kernel", sv["acc_rbf"], sv["acc70"]),
        ("one decision tree", tr["acc4"], tr["acc_tree70"]),
        ("random forest (200 trees)", None, tr["forest_acc"][-1]),
        ("gradient boosting (300 trees)", None, tr["boost_acc"][-1]),
        (f"lasso: {len(la['words5'])} words", None, la["acc5"]),
    ]
    return dict(rows=rows)


ITEMS = {
    "pages": compute_pages,
    "zipf": compute_zipf,
    "logistic": compute_logistic,
    "lasso": compute_lasso,
    "lda": compute_lda,
    "knn": compute_knn,
    "svm": compute_svm,
    "trees": compute_trees,
    "boost2": compute_boost2,
    "board": compute_board,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
