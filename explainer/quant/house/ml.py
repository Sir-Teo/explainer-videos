"""The House's machine learning for returns (Part 27).

**Market timing with many parameters.**  :func:`rff` (random Fourier features of a few predictors) and
:func:`ridge_dual` (ridge in its kernel form, exact when there are more features than observations) are the two pieces
of Kelly, Malamud and Zhou's (2024) "virtue of complexity"; :func:`kmz_timing` runs their rolling experiment over a
grid of complexities and shrinkages, and :func:`kernel_weights` shows Nagel's (2025) reading of the same forecast: in
the limit it is a weighted average of the training window's returns.

**The cross-section.**  Linear models (:func:`ols`, :func:`enet`, :func:`pcr`, :func:`pls`), boosted trees
(:class:`GBMRegressor`, the credit desk's trees with a squared loss), feed-forward networks with seed ensembles
(:class:`MLPEnsemble`), the conditional autoencoder of Gu, Kelly and Xiu (2021) (:class:`CondAutoencoder`), an
attention model across assets (:class:`CrossAttention`), a chart-image CNN after Jiang, Kelly and Xiu (2023)
(:func:`chart_images`, :class:`ChartCNN`) and an adversarially trained SDF after Chen, Pelger and Zhu (2024)
(:class:`AdversarialSDF`).  Scored by :func:`r2_oos` (against a forecast of zero, as Gu, Kelly and Xiu do) and by the
long-short spread of their predictions (:func:`decile_spread`).

**The practitioner's toolkit** (Lopez de Prado 2018): :func:`dollar_bars`, :func:`triple_barrier`, meta-labels,
:func:`fracdiff` and :func:`uniqueness_weights`; and :func:`split_conformal` / :func:`adaptive_conformal` for
prediction intervals with coverage guarantees.
"""

from __future__ import annotations

import math

import numpy as np

from explainer.quant.house.credit import GBM


# ---------------------------------------------------------------------------
# Market timing: random features and ridge
# ---------------------------------------------------------------------------
def rff(X, P: int, gamma: float = 2.0, seed=0) -> np.ndarray:
    """``P`` random Fourier features of the rows of ``X`` (T x d): sin and cos of X w_j, w_j ~ N(0, gamma^2 I), P/2
    of each, scaled by 1/sqrt(P) so that Z Z' is a Gaussian-kernel estimate (Rahimi and Recht 2007)."""
    X = np.asarray(X, float)
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((X.shape[1], max(P // 2, 1))) * gamma
    A = X @ W
    return np.hstack([np.sin(A), np.cos(A)])[:, :P] * math.sqrt(2.0 / P)


def ridge_dual(Z, y, z: float):
    """Ridge coefficients b = (Z'Z + z T I)^{-1} Z'y, computed as Z'(ZZ' + z T I)^{-1} y (T x T: cheap when P > T).
    As z -> 0 with P > T it is the minimum-norm interpolator, 'ridgeless' regression."""
    Z, y = np.asarray(Z, float), np.asarray(y, float)
    T = len(y)
    return Z.T @ np.linalg.solve(Z @ Z.T + z * T * np.eye(T), y)


def kmz_timing(X, r, T: int = 12, Ps=(2, 6, 12, 60, 120, 600, 1200, 6000, 12000), zs=(1e-3, 1e-1, 10.0, 1e3),
               gamma: float = 2.0, n_seeds: int = 5, start: int | None = None) -> dict:
    """Kelly, Malamud and Zhou's experiment: each month t, fit ridge on the last ``T`` months (predictors at s-1,
    returns at s) in ``P`` random features, forecast month t; the timing strategy holds the forecast times the
    return.  Averaged over ``n_seeds`` draws of the features.  Returns forecasts F[P][z] (months x 1) and the
    month index."""
    X, r = np.asarray(X, float), np.asarray(r, float)
    n = len(r)
    t0 = start if start is not None else T + 1
    out = {P: {z: np.full(n, np.nan) for z in zs} for P in Ps}
    Pmax = max(Ps)
    Zall = [rff(X, Pmax, gamma, seed=s) * math.sqrt(Pmax / 2) for s in range(n_seeds)]   # unscaled; rescaled per P
    for t in range(t0, n):
        tr = np.arange(t - T, t)            # predictors at s - 1 explain the return at s
        for P in Ps:
            idx = np.r_[np.arange(P // 2), Pmax // 2 + np.arange(P - P // 2)]
            acc = {z: 0.0 for z in zs}
            for Z in Zall:
                Zp = Z[np.r_[tr - 1, t - 1]][:, idx] / math.sqrt(P / 2)     # only the rows needed
                Ztr, y = Zp[:-1], r[tr]
                K = Ztr @ Ztr.T
                kz = Zp[-1] @ Ztr.T
                for z in zs:
                    a = np.linalg.solve(K + z * T * np.eye(T), y)
                    acc[z] += float(kz @ a) / len(Zall)
            for z in zs:
                out[P][z][t] = acc[z]
    return {"F": out, "t0": t0}


def kernel_weights(X, t: int, T: int = 12, gamma: float = 2.0) -> np.ndarray:
    """Nagel's reading: with P -> infinity and z -> 0, the RFF ridge forecast for month t is sum_s w_s r_s over the
    training window, with w = k(x_{t-1}, X)(K)^{-1}... for small T and the Gaussian kernel the weights are nearly
    proportional to the kernel similarities themselves.  Returns the T kernel similarities k(x_{t-1}, x_{s-1})."""
    X = np.asarray(X, float)
    tr = np.arange(t - T, t)
    d2 = ((X[tr - 1] - X[t - 1]) ** 2).sum(1)
    return np.exp(-0.5 * gamma ** 2 * d2)


# ---------------------------------------------------------------------------
# Linear models
# ---------------------------------------------------------------------------
def ols(X, y):
    X, y = np.asarray(X, float), np.asarray(y, float)
    A = np.column_stack([np.ones(len(X)), X])
    b = np.linalg.lstsq(A, y, rcond=None)[0]
    return lambda Z: np.column_stack([np.ones(len(Z)), np.asarray(Z, float)]) @ b


def enet(X, y, lam: float, alpha: float = 0.5, iters: int = 200):
    """Elastic net by coordinate descent on standardised X: (1/2n)|y - Xb|^2 + lam (alpha |b|_1 + (1-alpha)/2 |b|^2)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    mu, sd = X.mean(0), X.std(0) + 1e-12
    Xs = (X - mu) / sd
    ym = y.mean()
    yc = y - ym
    n, p = Xs.shape
    b = np.zeros(p)
    r = yc.copy()
    for _ in range(iters):
        for j in range(p):
            r += Xs[:, j] * b[j]
            rho = Xs[:, j] @ r / n
            b[j] = np.sign(rho) * max(abs(rho) - lam * alpha, 0) / (1 + lam * (1 - alpha))
            r -= Xs[:, j] * b[j]
    return lambda Z: ym + ((np.asarray(Z, float) - mu) / sd) @ b


def pcr(X, y, k: int):
    """Principal-components regression on the first ``k`` components of standardised X."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    mu, sd = X.mean(0), X.std(0) + 1e-12
    Xs = (X - mu) / sd
    _, _, Vt = np.linalg.svd(Xs, full_matrices=False)
    V = Vt[:k].T
    F = Xs @ V
    b = np.linalg.lstsq(np.column_stack([np.ones(len(F)), F]), y, rcond=None)[0]
    return lambda Z: b[0] + (((np.asarray(Z, float) - mu) / sd) @ V) @ b[1:]


def pls(X, y, k: int):
    """Partial least squares (NIPALS, one response): components chosen for their covariance with y."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    mu, sd, ym = X.mean(0), X.std(0) + 1e-12, y.mean()
    E, f = (X - mu) / sd, y - ym
    W, P, q = [], [], []
    for _ in range(k):
        w = E.T @ f
        w /= np.linalg.norm(w) + 1e-12
        t = E @ w
        tt = t @ t + 1e-12
        p_ = E.T @ t / tt
        qq = f @ t / tt
        E = E - np.outer(t, p_)
        f = f - qq * t
        W.append(w)
        P.append(p_)
        q.append(qq)
    W, P, q = np.array(W).T, np.array(P).T, np.array(q)
    B = W @ np.linalg.solve(P.T @ W, q)
    return lambda Z: ym + ((np.asarray(Z, float) - mu) / sd) @ B


# ---------------------------------------------------------------------------
# Trees
# ---------------------------------------------------------------------------
class GBMRegressor(GBM):
    """The credit desk's boosted trees with a squared loss: gradient F - y, Hessian 1, base the mean; optional
    early stopping on a validation set's mean squared error."""

    def fit(self, X, y, X_val=None, y_val=None, early_stop=None):
        X, y = np.asarray(X, float), np.asarray(y, float)
        rng = np.random.default_rng(self.seed)
        qs = np.linspace(0, 1, self.n_bins + 1)[1:-1]
        self.edges = [np.unique(np.nanquantile(X[:, j], qs)) for j in range(X.shape[1])]
        B = self._bin(X)
        self.base = float(y.mean())
        F = np.full(len(y), self.base)
        self.trees, self.val_loss = [], []
        Bv = self._bin(np.asarray(X_val, float)) if X_val is not None else None
        Fv = np.full(len(Bv), self.base) if Bv is not None else None
        best, best_n = np.inf, 0
        h = np.ones(len(y))
        for m in range(self.n_trees):
            g = F - y
            rows = np.where(rng.random(len(y)) < self.subsample)[0]
            cols = np.where(rng.random(X.shape[1]) < self.colsample)[0]
            if len(cols) == 0:
                cols = np.arange(X.shape[1])
            tree = self._grow(B, g, h, rows, cols, 0)
            self.trees.append(tree)
            F += self.lr * self._apply(tree, B)
            if Bv is not None:
                Fv += self.lr * self._apply(tree, Bv)
                mse = float(np.mean((np.asarray(y_val, float) - Fv) ** 2))
                self.val_loss.append(mse)
                if mse < best:
                    best, best_n = mse, m + 1
                elif early_stop and m + 1 - best_n >= early_stop:
                    break
        if Bv is not None and early_stop:
            self.trees = self.trees[:max(best_n, 1)]
        return self

    def predict(self, X):
        return self.decision(X)


# ---------------------------------------------------------------------------
# Networks (torch)
# ---------------------------------------------------------------------------
def _torch():
    import torch
    torch.set_num_threads(2)
    return torch


def _mlp(d_in, hidden, d_out=1, dropout=0.0):
    torch = _torch()
    layers, d = [], d_in
    for h in hidden:
        layers += [torch.nn.Linear(d, h), torch.nn.SiLU()]
        if dropout:
            layers.append(torch.nn.Dropout(dropout))
        d = h
    layers.append(torch.nn.Linear(d, d_out))
    return torch.nn.Sequential(*layers)


def _train(model, loss_fn, batches, params, epochs, lr, l1=0.0, val=None, patience=5, log=None):
    """A generic loop: Adam, an L1 penalty on the weights, early stopping on ``val()`` (lower is better)."""
    torch = _torch()
    opt = torch.optim.Adam(params, lr=lr)
    best, best_state, bad = np.inf, None, 0
    for ep in range(epochs):
        model.train()
        tot = 0.0
        for b in batches():
            opt.zero_grad()
            loss = loss_fn(*b)
            if l1:
                loss = loss + l1 * sum(p.abs().sum() for n_, p in model.named_parameters() if "weight" in n_)
            loss.backward()
            opt.step()
            tot += float(loss)
        if log is not None:
            log.append(tot)
        if val is not None:
            model.eval()
            with torch.no_grad():
                v = float(val())
            if v < best - 1e-9:
                best, bad = v, 0
                best_state = {k: t.clone() for k, t in model.state_dict().items()}
            else:
                bad += 1
                if bad >= patience:
                    break
    if best_state is not None:
        model.load_state_dict(best_state)
    return model


class MLPEnsemble:
    """Feed-forward networks for E[r | x], one per seed, averaged (Gu, Kelly and Xiu's NN1-NN5: hidden layers of 32,
    16, 8, 4, 2 units). Trained by Adam on mean squared error with an L1 penalty and early stopping on validation."""

    def __init__(self, hidden=(32, 16, 8), seeds=(0, 1, 2, 3, 4), epochs=60, lr=1e-3, l1=1e-5, batch=512):
        self.hidden, self.seeds, self.epochs, self.lr, self.l1, self.batch = hidden, seeds, epochs, lr, l1, batch

    def fit(self, X, y, Xv=None, yv=None):
        torch = _torch()
        Xt, yt = torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)
        Xvt = torch.tensor(Xv, dtype=torch.float32) if Xv is not None else None
        yvt = torch.tensor(yv, dtype=torch.float32) if yv is not None else None
        self.nets = []
        for s in self.seeds:
            torch.manual_seed(s)
            net = _mlp(X.shape[1], self.hidden)
            g = torch.Generator().manual_seed(s)

            def batches(net=net, g=g):
                perm = torch.randperm(len(Xt), generator=g)
                for i in range(0, len(Xt), self.batch):
                    j = perm[i:i + self.batch]
                    yield Xt[j], yt[j]
            loss = lambda xb, yb, net=net: torch.mean((net(xb).squeeze(-1) - yb) ** 2)  # noqa: E731
            val = (lambda net=net: torch.mean((net(Xvt).squeeze(-1) - yvt) ** 2)) if Xvt is not None else None
            self.nets.append(_train(net, loss, batches, net.parameters(), self.epochs, self.lr, self.l1, val))
        return self

    def predict(self, X):
        torch = _torch()
        Xt = torch.tensor(np.asarray(X, float), dtype=torch.float32)
        with torch.no_grad():
            return np.mean([n(Xt).squeeze(-1).numpy() for n in self.nets], axis=0)


class CondAutoencoder:
    """Gu, Kelly and Xiu's (2021) conditional autoencoder: r_{i,t} = beta(z_{i,t-1})' f_t.  Betas are a network of each
    asset's lagged characteristics; factors are linear combinations of characteristic-managed portfolios
    x_t = Z_{t-1}' r_t / N_t.  Fitted to minimise the squared pricing error over panels given as lists of (Z_t, r_t)."""

    def __init__(self, K=3, hidden=(32,), epochs=60, lr=3e-3, seed=0, l1=1e-5):
        self.K, self.hidden, self.epochs, self.lr, self.seed, self.l1 = K, hidden, epochs, lr, seed, l1

    def _net(self, d):
        torch = _torch()
        torch.manual_seed(self.seed)
        self.beta = _mlp(d, self.hidden, self.K)
        self.fac = torch.nn.Linear(d, self.K, bias=False)
        return torch.nn.ModuleList([self.beta, self.fac])

    def fit(self, panels, val=None):
        torch = _torch()
        P = [(torch.tensor(Z, dtype=torch.float32), torch.tensor(r, dtype=torch.float32)) for Z, r in panels]
        V = [(torch.tensor(Z, dtype=torch.float32), torch.tensor(r, dtype=torch.float32)) for Z, r in (val or [])]
        model = self._net(P[0][0].shape[1])
        rng = np.random.default_rng(self.seed)

        def batches():
            for k in rng.permutation(len(P)):
                yield P[k]

        def loss(Z, r):
            x = Z.T @ r / len(r)                     # managed portfolios
            f = self.fac(x)
            return torch.mean((r - self.beta(Z) @ f) ** 2)
        vf = (lambda: sum(float(loss(Z, r)) for Z, r in V) / len(V)) if V else None
        _train(model, loss, batches, model.parameters(), self.epochs, self.lr, self.l1, vf)
        return self

    def predict(self, Z, lam):
        """The predictive version: beta(z_{i,t-1})' lambda, with lambda the average factor realisation in training."""
        torch = _torch()
        with torch.no_grad():
            return (self.beta(torch.tensor(Z, dtype=torch.float32)) @ torch.tensor(lam, dtype=torch.float32)).numpy()

    def factors(self, Z, r):
        torch = _torch()
        with torch.no_grad():
            Zt, rt = torch.tensor(Z, dtype=torch.float32), torch.tensor(r, dtype=torch.float32)
            return self.fac(Zt.T @ rt / len(rt)).numpy()

    def fitted(self, Z, r):
        torch = _torch()
        with torch.no_grad():
            Zt, rt = torch.tensor(Z, dtype=torch.float32), torch.tensor(r, dtype=torch.float32)
            return (self.beta(Zt) @ self.fac(Zt.T @ rt / len(rt))).numpy()


class CrossAttention:
    """A small transformer encoder across the assets of one date: each asset's characteristics are embedded, a few
    heads of self-attention let every asset's forecast depend on every other's (permutation equivariant, any number
    of assets), and a head maps to the forecast.  Trained on panels of (Z_t, r_t) by mean squared error."""

    def __init__(self, d_model=32, heads=4, layers=1, epochs=40, lr=1e-3, seed=0):
        self.d, self.h, self.L, self.epochs, self.lr, self.seed = d_model, heads, layers, epochs, lr, seed

    def fit(self, panels, val=None):
        torch = _torch()
        torch.manual_seed(self.seed)
        d_in = panels[0][0].shape[1]
        enc = torch.nn.TransformerEncoder(torch.nn.TransformerEncoderLayer(self.d, self.h, 2 * self.d, dropout=0.0,
                                                                         batch_first=True), self.L)
        self.model = torch.nn.ModuleList([torch.nn.Linear(d_in, self.d), enc, torch.nn.Linear(self.d, 1)])
        P = [(torch.tensor(Z, dtype=torch.float32), torch.tensor(r, dtype=torch.float32)) for Z, r in panels]
        V = [(torch.tensor(Z, dtype=torch.float32), torch.tensor(r, dtype=torch.float32)) for Z, r in (val or [])]
        rng = np.random.default_rng(self.seed)

        def batches():
            for k in rng.permutation(len(P)):
                yield P[k]
        loss = lambda Z, r: torch.mean((self._f(Z) - r) ** 2)  # noqa: E731
        vf = (lambda: sum(float(loss(Z, r)) for Z, r in V) / len(V)) if V else None
        _train(self.model, loss, batches, self.model.parameters(), self.epochs, self.lr, 0.0, vf)
        return self

    def _f(self, Z):
        emb, enc, head = self.model
        return head(enc(emb(Z).unsqueeze(0))).squeeze(0).squeeze(-1)

    def predict(self, Z):
        torch = _torch()
        with torch.no_grad():
            return self._f(torch.tensor(Z, dtype=torch.float32)).numpy()

    def attention(self, Z):
        """The first layer's attention weights (heads averaged): which assets each asset's forecast looks at."""
        torch = _torch()
        emb, enc, _ = self.model
        layer = enc.layers[0]
        with torch.no_grad():
            x = emb(torch.tensor(Z, dtype=torch.float32)).unsqueeze(0)
            _, w = layer.self_attn(x, x, x, need_weights=True, average_attn_weights=True)
        return w.squeeze(0).numpy()


def chart_images(o, h, l, c, v, t: int, days: int = 20, height: int = 32) -> np.ndarray:
    """Jiang, Kelly and Xiu's (2023) price image for the ``days`` up to and including t: three pixel columns a day
    (open tick, high-low bar, close tick), a moving average line, and volume bars in the bottom fifth; black and
    white, ``height`` x 3*days."""
    W = 3 * days
    img = np.zeros((height, W), np.float32)
    s = slice(t - days + 1, t + 1)
    O, H, L, C, V = o[s], h[s], l[s], c[s], v[s]
    ma = np.array([c[max(0, k - days + 1):k + 1].mean() for k in range(t - days + 1, t + 1)])
    lo, hi = min(L.min(), ma.min()), max(H.max(), ma.max())
    top = int(height * 0.8)

    def row(p):
        return int(round((top - 1) * (1 - (p - lo) / max(hi - lo, 1e-12))))
    vmax = max(V.max(), 1e-12)
    for k in range(days):
        x = 3 * k
        img[row(O[k]), x] = 1
        img[row(H[k]):row(L[k]) + 1, x + 1] = 1
        img[row(C[k]), x + 2] = 1
        img[row(ma[k]), x:x + 3] = np.maximum(img[row(ma[k]), x:x + 3], 1)
        vh = int(round((height - top - 1) * V[k] / vmax))
        if vh > 0:
            img[height - vh:, x + 1] = 1
    return img


class ChartCNN:
    """A small convolutional network on chart images: two conv blocks and a linear head, predicting the probability
    that the next period's return is positive (cross-entropy), as Jiang, Kelly and Xiu do."""

    def __init__(self, epochs=12, lr=1e-3, seed=0, batch=256):
        self.epochs, self.lr, self.seed, self.batch = epochs, lr, seed, batch

    def fit(self, imgs, y, imgs_v=None, y_v=None):
        torch = _torch()
        torch.manual_seed(self.seed)
        nn = torch.nn
        H, W = imgs.shape[1:]
        self.net = nn.Sequential(nn.Conv2d(1, 16, (5, 3), padding=(2, 1)), nn.BatchNorm2d(16), nn.LeakyReLU(),
                                 nn.MaxPool2d((2, 1)), nn.Conv2d(16, 32, (5, 3), padding=(2, 1)), nn.BatchNorm2d(32),
                                 nn.LeakyReLU(), nn.MaxPool2d((2, 1)), nn.Flatten(), nn.Dropout(0.5),
                                 nn.Linear(32 * (H // 4) * W, 1))
        X = torch.tensor(imgs[:, None], dtype=torch.float32)
        Y = torch.tensor(y, dtype=torch.float32)
        Xv = torch.tensor(imgs_v[:, None], dtype=torch.float32) if imgs_v is not None else None
        Yv = torch.tensor(y_v, dtype=torch.float32) if y_v is not None else None
        g = torch.Generator().manual_seed(self.seed)
        bce = torch.nn.BCEWithLogitsLoss()

        def batches():
            perm = torch.randperm(len(X), generator=g)
            for i in range(0, len(X), self.batch):
                j = perm[i:i + self.batch]
                yield X[j], Y[j]
        loss = lambda xb, yb: bce(self.net(xb).squeeze(-1), yb)  # noqa: E731
        val = (lambda: bce(self.net(Xv).squeeze(-1), Yv)) if Xv is not None else None
        _train(self.net, loss, batches, self.net.parameters(), self.epochs, self.lr, 0.0, val, patience=3)
        return self

    def predict_proba(self, imgs):
        torch = _torch()
        self.net.eval()
        out = []
        with torch.no_grad():
            for i in range(0, len(imgs), 2048):
                out.append(torch.sigmoid(self.net(torch.tensor(imgs[i:i + 2048, None], dtype=torch.float32))
                                         ).squeeze(-1).numpy())
        return np.concatenate(out)


class AdversarialSDF:
    """Chen, Pelger and Zhu's (2024) idea, small: SDF weights w(z_i) from a network of each asset's characteristics,
    M_{t+1} = 1 - sum_i w_i R_{i,t+1}; a second network g(z_i) chooses the test assets (conditional moments
    E[M R_i g(z_i)] = 0) that the SDF prices worst, and the two are trained against each other."""

    def __init__(self, hidden=(32, 16), n_moments=4, epochs=40, lr=1e-3, seed=0, rounds=3):
        self.hidden, self.M, self.epochs, self.lr, self.seed, self.rounds = hidden, n_moments, epochs, lr, seed, rounds

    def fit(self, panels):
        torch = _torch()
        torch.manual_seed(self.seed)
        d = panels[0][0].shape[1]
        self.w = _mlp(d, self.hidden)
        self.g = torch.nn.Sequential(_mlp(d, (16,), self.M), torch.nn.Tanh())
        P = [(torch.tensor(Z, dtype=torch.float32), torch.tensor(r, dtype=torch.float32)) for Z, r in panels]

        def moments():
            errs = []
            for Z, r in P:
                w = self.w(Z).squeeze(-1)
                w = w / (w.abs().sum() + 1e-6)
                m = 1 - (w * r).sum()
                errs.append((m * r[:, None] * self.g(Z)).mean(0))
            return torch.stack(errs).mean(0)
        opt_w = torch.optim.Adam(self.w.parameters(), lr=self.lr)
        opt_g = torch.optim.Adam(self.g.parameters(), lr=self.lr)
        for _ in range(self.rounds):
            for _ in range(self.epochs):          # the SDF minimises the worst moments
                opt_w.zero_grad()
                (moments() ** 2).sum().backward()
                opt_w.step()
            for _ in range(self.epochs // 2):     # the adversary finds the moments it fails most
                opt_g.zero_grad()
                (-(moments() ** 2).sum()).backward()
                opt_g.step()
        return self

    def weights(self, Z):
        torch = _torch()
        with torch.no_grad():
            w = self.w(torch.tensor(Z, dtype=torch.float32)).squeeze(-1)
            return (w / (w.abs().sum() + 1e-6)).numpy()


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
def r2_oos(y, yhat) -> float:
    """Gu, Kelly and Xiu's out-of-sample R^2: 1 - sum (y - yhat)^2 / sum y^2, against a forecast of zero (not the
    historical mean, which is too noisy to be a benchmark for individual assets)."""
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    return float(1 - np.sum((y - yhat) ** 2) / np.sum(y ** 2))


def decile_spread(dates, pred, ret, q: int = 10, weights=None) -> dict:
    """Each date, sort assets by prediction into ``q`` groups; the long-short return of top minus bottom (equal or
    ``weights``-weighted), date by date."""
    dates, pred, ret = np.asarray(dates), np.asarray(pred, float), np.asarray(ret, float)
    out_d, out_r = [], []
    for d in np.unique(dates):
        m = dates == d
        if m.sum() < 2 * q:
            continue
        p, r = pred[m], ret[m]
        w = np.ones(m.sum()) if weights is None else np.asarray(weights, float)[m]
        k = np.argsort(np.argsort(p)) * q // m.sum()
        hi, lo = k == q - 1, k == 0
        out_d.append(d)
        out_r.append(np.average(r[hi], weights=w[hi]) - np.average(r[lo], weights=w[lo]))
    return {"date": np.array(out_d), "ls": np.array(out_r)}


# ---------------------------------------------------------------------------
# The practitioner's toolkit (Lopez de Prado 2018)
# ---------------------------------------------------------------------------
def dollar_bars(t, close, dollar_volume, threshold: float) -> dict:
    """Information-driven bars: a new bar closes each time cumulative traded value passes ``threshold``, so bars are
    frequent when the market is busy and rare when it is quiet."""
    t, c, dv = np.asarray(t), np.asarray(close, float), np.asarray(dollar_volume, float)
    cum = np.cumsum(dv)
    k = np.floor(cum / threshold + 1e-12).astype(int)
    ends = np.flatnonzero(np.diff(np.r_[0, k]) > 0)       # the step at which each threshold is crossed
    return {"t": t[ends], "close": c[ends], "idx": ends}


def triple_barrier(close, vol, horizon: int, up: float = 2.0, down: float = 2.0) -> dict:
    """For each start, the first of three barriers the price touches: up ``up`` x vol (+1), down ``down`` x vol (-1),
    or ``horizon`` steps (the sign of the return then, or 0).  Returns labels and when each label was decided."""
    c, v = np.asarray(close, float), np.asarray(vol, float)
    n = len(c)
    lab, end = np.zeros(n, int), np.full(n, n - 1)
    for i in range(n - 1):
        j1 = min(i + horizon, n - 1)
        path = c[i + 1:j1 + 1] / c[i] - 1
        hu = np.flatnonzero(path >= up * v[i])
        hd = np.flatnonzero(path <= -down * v[i])
        a = hu[0] if len(hu) else np.inf
        b = hd[0] if len(hd) else np.inf
        if a < b:
            lab[i], end[i] = 1, i + 1 + int(a)
        elif b < a:
            lab[i], end[i] = -1, i + 1 + int(b)
        else:
            lab[i], end[i] = int(np.sign(path[-1])) if len(path) else 0, j1
    return {"label": lab, "end": end}


def uniqueness_weights(start, end, n: int) -> np.ndarray:
    """Average uniqueness of each label: 1 / (number of concurrent labels), averaged over the label's span. Labels
    that overlap many others carry less independent information and get less weight."""
    conc = np.zeros(n)
    for a, b in zip(start, end):
        conc[a:b + 1] += 1
    return np.array([np.mean(1 / conc[a:b + 1]) for a, b in zip(start, end)])


def fracdiff_weights(d: float, thresh: float = 1e-4, max_len: int = 10_000) -> np.ndarray:
    w = [1.0]
    k = 1
    while k < max_len:
        w_ = -w[-1] * (d - k + 1) / k
        if abs(w_) < thresh:
            break
        w.append(w_)
        k += 1
    return np.array(w)


def fracdiff(x, d: float, thresh: float = 1e-4) -> np.ndarray:
    """Fixed-window fractional differencing: (1 - L)^d x, truncated where the weights fall below ``thresh``. d = 0 is
    the price, d = 1 its change; in between, a series that is stationary but remembers its level."""
    x = np.asarray(x, float)
    w = fracdiff_weights(d, thresh)
    out = np.full(len(x), np.nan)
    L = len(w)
    for t in range(L - 1, len(x)):
        out[t] = w @ x[t - L + 1:t + 1][::-1]
    return out


# ---------------------------------------------------------------------------
# Conformal prediction
# ---------------------------------------------------------------------------
def split_conformal(resid_cal, alpha: float = 0.1) -> float:
    """The split-conformal half-width: the ceil((n + 1)(1 - alpha))/n quantile of the calibration set's absolute
    residuals. If calibration and test points are exchangeable, [yhat - q, yhat + q] covers with probability at
    least 1 - alpha (Vovk et al. 2005; Lei et al. 2018)."""
    r = np.sort(np.abs(np.asarray(resid_cal, float)))
    n = len(r)
    k = min(int(math.ceil((n + 1) * (1 - alpha))), n) - 1
    return float(r[k])


def adaptive_conformal(resid_stream, alpha: float = 0.1, gamma: float = 0.005, window: int = 250) -> dict:
    """Gibbs and Candes's (2021) adaptive conformal inference for a series that is not exchangeable: the working
    level alpha_t is nudged after each miss or hit, alpha_{t+1} = alpha_t + gamma (alpha - err_t), so long-run
    coverage is 1 - alpha whatever the drift. Half-widths from the last ``window`` absolute residuals."""
    r = np.abs(np.asarray(resid_stream, float))
    a = alpha
    q, cover = np.full(len(r), np.nan), np.full(len(r), np.nan)
    for t in range(window, len(r)):
        past = np.sort(r[t - window:t])
        lev = min(max(1 - a, 0.0), 1.0)
        q[t] = past[min(int(math.ceil(lev * (window + 1))) - 1, window - 1)] if lev > 0 else 0.0
        err = float(r[t] > q[t])
        cover[t] = 1 - err
        a = a + gamma * (alpha - err)
    return {"q": q, "cover": cover}
