"""Precompute everything numerical in Part 8 of the AI series ("Fitting and Generalizing").

    python -m videos.ai.ai8.compute              # everything missing (needs Part 6's pages: .cache/ai6)
    python -m videos.ai.ai8.compute --force double

Results are cached in ``.cache/ai8/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Everything is small and
runs on one CPU core (about an hour in all); every random choice is seeded.  The memorization item reads the series'
novels model (``explainer.ai.novels``, trained once for Parts 18, 19, 27 and 30).

Items:
    gap        the training error and the test error of Part 6's k-nearest-neighbour vote, k = 1 ... 151
    risk       risk, empirical risk and Bayes risk on two Gaussian classes; threshold rules learned from n examples
    biasvar    bias and variance by resampling: polynomials of degree 0 ... 15 fitted to 200 fresh samples of 16 noisy
               points from one curve (illustrative); bias squared + variance + noise = the measured test error
    hoeffding  sample means of a biased coin, 100,000 times at each n: histograms, tails, Hoeffding and Chebyshev
    union      K useless rules on coin-flip labels: the best one's training score, the worst gap, the union bound
    shatter    lines in the plane: all 8 labellings of 3 points are separable, 2 of the 16 labellings of 4 are not
    growth     growth functions counted: half-planes on n points, intervals on a line, against Sauer-Shelah and 2^n
    rademacher how well linear classifiers on the first d of Part 6's 70 rates can fit random signs, d = 1 ... 70
    radlin     the empirical Rademacher complexity of norm-bounded linear functions on the pages, against its bound
    margins    a support vector machine on the pages, its margins and the margin bound; AdaBoost's margins
    pacbayes   a PAC-Bayes bound (Dziugaite & Roy's recipe) for a 70 -> 128 -> 1 network on the pages
    stability  uniform stability of ridge regression, measured; SGD's two runs drifting apart (Hardt et al.)
    compress   support vectors as a compression scheme, and its bound, on separable points and on the pages
    random     one network (70 -> 512 -> 512 -> 2) trained on Part 6's pages with the true and with shuffled authors
    corrupt    the same network with 0 ... 100% of the labels shuffled: time to fit, and accuracy on new pages
    minnorm    gradient descent on underdetermined least squares converges to the pseudoinverse solution
    maxmargin  gradient descent on the logistic loss: the direction tends to the max-margin one, at rate 1/log t
    double     double descent: least squares on p random features of the pages, test error and the smallest
               singular value against p; ridge
    samplewise more data can hurt: p = 200 fixed random features, n = 20 ... 448 training pages
    epochwise  gradient descent on a linear model with two feature scales: test error dips, rises, falls again
    benign     benign overfitting: the minimum-norm interpolant with a spiked covariance against an isotropic one
    sharp      sharpness against generalization: small networks trained with SGD at several batch sizes; the
               rescaling that changes sharpness and nothing else
    shift      covariate shift: least squares, importance-weighted least squares, and estimated weights
    memorize   the novels model: how often it reproduces a 32-token passage of its training text from the 32
               tokens before it, against how many times the passage occurs
    canary     the novels model trained on, with held-out passages planted 1 ... 64 times: extraction against
               repetition, through training (checkpointed; about forty minutes on two threads)
"""

from __future__ import annotations

import math
import os
import time

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai8")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _torch():
    """torch with this part's thread budget (set here, never at import time)."""
    import torch

    torch.set_num_threads(int(os.environ.get("AI8_THREADS", "1")))
    return torch


def pages():
    from videos.ai.ai6 import compute as c5

    p = c5.load("pages")
    X, y, test = np.asarray(p["X"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
    mu, sd = X[~test].mean(0), X[~test].std(0) + 1e-9
    Z = (X - mu) / sd
    return Z[~test], y[~test], Z[test], y[test], np.asarray(p["X2"])


def kl_bin(p: float, q: float) -> float:
    p, q = min(max(p, 1e-12), 1 - 1e-12), min(max(q, 1e-12), 1 - 1e-12)
    return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))


def kl_inv(p: float, c: float) -> float:
    """The largest q >= p with kl(p || q) <= c (bisection)."""
    lo, hi = p, 1.0
    for _ in range(100):
        m = 0.5 * (lo + hi)
        if kl_bin(p, m) > c:
            hi = m
        else:
            lo = m
    return lo


def vc_bound(d: float, n: float, delta: float = 0.05) -> float:
    """The VC bound's gap term as on screen: sqrt((d (ln(2n/d) + 1) + ln(4/delta)) / n)."""
    return math.sqrt((d * (math.log(2 * n / d) + 1) + math.log(4 / delta)) / n)


# ---------------------------------------------------------------------------
def compute_gap():
    _, ytr, _, yte, X2 = pages()
    from videos.ai.ai6 import compute as c5

    p = c5.load("pages")
    test = np.asarray(p["test"], bool)
    A, B, _, _ = c5.standardize(X2[~test], X2[test])  # exactly as Part 6 did (the rates tie often; ties must break alike)
    dAA = ((A[:, None] - A[None]) ** 2).sum(-1)
    dBA = ((B[:, None] - A[None]) ** 2).sum(-1)
    oA, oB = np.argsort(dAA, 1, kind="stable"), np.argsort(dBA, 1, kind="stable")
    ks = np.arange(1, 152, 2)
    tr = [float(((ytr[oA[:, :k]].mean(1) > 0.5) == ytr).mean()) for k in ks]
    te = [float(((ytr[oB[:, :k]].mean(1) > 0.5) == yte).mean()) for k in ks]
    best = int(ks[int(np.argmax(te))])
    return dict(ks=ks, train_err=1 - np.array(tr), test_err=1 - np.array(te), best_k=best)


# ---------------------------------------------------------------------------
RISK = dict(m1=1.0, s1=0.6, m0=-0.3, s0=1.5)  # class 1 narrow, class 0 wide: the Bayes rule is an interval


def compute_risk():
    """Two classes, equally likely: x | y=1 ~ N(1, 0.6^2), x | y=0 ~ N(-0.3, 1.5^2).  The Bayes rule says 1 on an
    interval; the learner may only use thresholds, "1 if x > t".  Risk of a threshold is exact (normal CDFs)."""
    from scipy.stats import norm

    m1, s1, m0, s0 = RISK["m1"], RISK["s1"], RISK["m0"], RISK["s0"]
    xg = np.linspace(-5.0, 5.0, 20001)
    dx = xg[1] - xg[0]
    p1, p0 = 0.5 * norm.pdf(xg, m1, s1), 0.5 * norm.pdf(xg, m0, s0)
    bayes = float(np.minimum(p0, p1).sum() * dx)
    inside = p1 > p0
    a, b = float(xg[inside][0]), float(xg[inside][-1])

    def R(t):
        t = np.asarray(t, float)
        return 0.5 * (1 - norm.cdf((t - m0) / s0)) + 0.5 * norm.cdf((t - m1) / s1)

    tt = np.linspace(-4, 4, 80001)
    t_star = float(tt[int(np.argmin(R(tt)))])
    r_class = float(R(t_star))
    g = rng(1967)  # Cover & Hart, 1967: nearest neighbours and the Bayes risk
    ns = [10, 20, 40, 80, 160, 320, 640, 1280, 2560]
    draws = 400
    emp, true, thr = [], [], []

    def draw(n):
        y = g.random(n) < 0.5
        x = np.where(y, g.normal(m1, s1, n), g.normal(m0, s0, n))
        return x, y

    def erm(x, y):
        o = np.argsort(x)
        xs, ys = x[o], y[o]
        # errors of "1 if x > t" with t below all points, then between consecutive points, then above all
        errs = np.concatenate([[np.sum(~ys)], np.sum(~ys) - np.cumsum(~ys) + np.cumsum(ys)])
        k = int(np.argmin(errs))
        t = xs[0] - 1 if k == 0 else (xs[-1] + 1 if k == len(xs) else 0.5 * (xs[k - 1] + xs[k]))
        return float(t), float(errs[k] / len(x))

    for n in ns:
        e_, r_, t_ = [], [], []
        for _ in range(draws):
            x, y = draw(n)
            t, e = erm(x, y)
            e_.append(e)
            r_.append(float(R(t)))
            t_.append(t)
        emp.append(e_)
        true.append(r_)
        thr.append(t_)
    emp, true = np.array(emp), np.array(true)
    x40, y40 = draw(40)
    t40 = np.array(thr[ns.index(40)][:30])
    assert np.all(true >= r_class - 1e-9) and r_class > bayes
    return dict(xg=xg[::40], p1=p1[::40], p0=p0[::40], bayes=bayes, a=a, b=b, t_star=t_star, r_class=r_class,
                ns=ns, emp_mean=emp.mean(1), true_mean=true.mean(1), true_q=np.quantile(true, [0.1, 0.9], axis=1),
                emp_q=np.quantile(emp, [0.1, 0.9], axis=1), draws=draws, x40=x40, y40=y40.astype(int), t40=t40,
                **RISK)


# ---------------------------------------------------------------------------
def truth(x):
    return np.sin(2.4 * x) + 0.3 * x


def compute_biasvar():
    g = rng(1992)  # Geman, Bienenstock & Doursat, 1992
    n, sigma, degs, runs = 16, 0.35, list(range(0, 16)), 200
    xg = np.linspace(-1.5, 1.5, 160)  # judged between the points, never beyond them
    fits = {d: [] for d in degs}
    mse = {d: [] for d in degs}
    xs_all = []
    for _ in range(runs):
        x = np.linspace(-1.6, 1.6, n) + g.uniform(-0.06, 0.06, n)
        yv = truth(x) + sigma * g.normal(size=n)
        ynew = truth(xg) + sigma * g.normal(size=len(xg))  # fresh noisy answers where the fit is judged
        xs_all.append((x, yv))
        for d in degs:
            V = np.vander(x / 1.6, d + 1)
            c = np.linalg.lstsq(V, yv, rcond=None)[0]
            f = np.vander(xg / 1.6, d + 1) @ c
            fits[d].append(f)
            mse[d].append(float(((f - ynew) ** 2).mean()))
    bias2, var = [], []
    for d in degs:
        F = np.array(fits[d])
        mean = F.mean(0)
        bias2.append(float(((mean - truth(xg)) ** 2).mean()))
        var.append(float(F.var(0).mean()))
    bias2, var = np.array(bias2), np.array(var)
    total = bias2 + var + sigma ** 2
    measured = np.array([np.mean(mse[d]) for d in degs])
    best = int(np.argmin(total))
    assert 3 <= best <= 9 and var[-1] > 100 * var[best] and bias2[0] > 10 * bias2[best]
    return dict(degs=degs, bias2=bias2, var=var, noise=sigma ** 2, total=total, measured=measured, best=best, xg=xg,
                truth=truth(xg), sample_x=xs_all[0][0], sample_y=xs_all[0][1], fits_1=np.array(fits[1][:20]),
                fits_best=np.array(fits[best][:20]), fits_top=np.array(fits[12][:20]), top=12, n=n, runs=runs,
                sigma=sigma)


# ---------------------------------------------------------------------------
def compute_hoeffding():
    """The mean of n flips of a coin that lands heads 30% of the time (a classifier's error rate on n test cases),
    drawn 100,000 times at each n; its tail against Hoeffding's and Chebyshev's bounds (Part 5 derives both)."""
    from scipy.stats import binom

    g = rng(1963)  # Hoeffding, 1963
    p, draws = 0.3, 100_000
    ns = [10, 40, 160, 640]
    eps = np.round(np.arange(0.0, 0.301, 0.01), 3)
    out = dict(p=p, draws=draws, ns=ns, eps=eps)
    for n in ns:
        k = g.binomial(n, p, draws)
        out[f"pmf{n}"] = np.bincount(k, minlength=n + 1) / draws
        dev = np.abs(k / n - p)
        out[f"tail{n}"] = np.array([float((dev >= e - 1e-12).mean()) for e in eps])
        out[f"hoef{n}"] = np.minimum(1.0, 2 * np.exp(-2 * n * eps ** 2))
        out[f"cheb{n}"] = np.minimum(1.0, p * (1 - p) / (n * np.maximum(eps, 1e-9) ** 2))
    # how many test cases make "within 5 points, 95% of the time" sure: Hoeffding's n against the exact one
    e, d = 0.05, 0.05
    n_hoef = int(math.ceil(math.log(2 / d) / (2 * e * e)))
    n_exact = next(n for n in range(10, 5000) if
                   binom.cdf(math.floor(n * (p + e) - 1e-9), n, p) - binom.cdf(math.ceil(n * (p - e) + 1e-9) - 1, n, p)
                   >= 1 - d)
    n_cheb = int(math.ceil(p * (1 - p) / (d * e * e)))
    out.update(n_hoef=n_hoef, n_exact=n_exact, n_cheb=n_cheb)
    return out


# ---------------------------------------------------------------------------
def compute_union():
    """K rules that know nothing, scored on n examples whose labels are coin flips: each rule's error is Bin(n, 1/2)/n,
    independently.  The best rule's training error and the largest gap |train - true| over the K rules, exactly
    (from the binomial distribution), against the union bound."""
    from scipy.stats import binom

    delta = 0.05
    Ks = [1, 10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6]
    out = dict(Ks=Ks, delta=delta, ns=[100, 1000])
    for n in (100, 1000):
        k = np.arange(n + 1)
        sf = binom.sf(k - 1, n, 0.5)  # P(errors >= k)
        best_med, gap95, bound = [], [], []
        dev = np.abs(k / n - 0.5)
        pm = binom.pmf(k, n, 0.5)
        for K in Ks:
            cdf_min = 1 - sf ** K  # P(min errors <= k)
            best_med.append(float(k[np.searchsorted(cdf_min, 0.5)] / n))
            # P(max gap < e) = P(|dev| < e)^K; the 95% quantile of the largest gap
            es = np.unique(dev)
            within = np.array([pm[dev < e + 1e-12].sum() for e in es])
            gap95.append(float(es[np.searchsorted(within ** K, 0.95)]))
            bound.append(math.sqrt(math.log(2 * K / delta) / (2 * n)))
        out[f"best{n}"] = np.array(best_med)
        out[f"gap{n}"] = np.array(gap95)
        out[f"bound{n}"] = np.array(bound)
    g = rng(1984)  # Valiant, 1984
    errs = g.binomial(100, 0.5, 1000) / 100
    out.update(sample_errs=errs, sample_best=float(errs.min()), sample_K=1000, sample_n=100)
    # the same best rule on 10,000 fresh examples: its true error is 1/2
    out["fresh_best"] = float(g.binomial(10_000, 0.5) / 10_000)
    return out


# ---------------------------------------------------------------------------
def separable(P, s):
    """Is there a line w.x + b with sign = s at every point?  (A tiny linear program, by brute force over normals.)"""
    for th in np.linspace(0, 2 * math.pi, 3600, endpoint=False):
        w = np.array([math.cos(th), math.sin(th)])
        proj = P @ w
        pos, neg = proj[s > 0], proj[s < 0]
        if len(pos) == 0 or len(neg) == 0 or pos.min() > neg.max() + 1e-9:
            return True
    return False


def compute_shatter():
    P3 = np.array([[-1.0, -0.7], [1.0, -0.7], [0.0, 0.9]])
    P4 = np.array([[-1.0, -1.0], [1.0, -1.0], [1.0, 1.0], [-1.0, 1.0]])
    labs3 = [np.array([1 if (k >> i) & 1 else -1 for i in range(3)]) for k in range(8)]
    labs4 = [np.array([1 if (k >> i) & 1 else -1 for i in range(4)]) for k in range(16)]
    ok3 = [separable(P3, s) for s in labs3]
    ok4 = [separable(P4, s) for s in labs4]
    assert all(ok3) and sum(not o for o in ok4) == 2  # the two XOR labellings
    return dict(P3=P3, P4=P4, labs3=np.array(labs3), labs4=np.array(labs4), ok3=ok3, ok4=ok4)


def halfplane_dichotomies(P) -> set:
    """Every labelling of the points P (n x 2) that some half-plane realizes, exactly: between two directions at which
    a pair of points swaps order, the order of the projections is fixed, and a threshold cuts it n + 1 ways."""
    n = len(P)
    if n < 2:
        return {0, 1} if n == 1 else {0}
    crit = []
    for i in range(n):
        for j in range(i + 1, n):
            d = P[i] - P[j]
            a = math.atan2(d[1], d[0]) + math.pi / 2
            crit += [a % (2 * math.pi), (a + math.pi) % (2 * math.pi)]
    crit = np.sort(np.array(crit))
    mids = (crit + np.roll(crit, -1)) / 2
    mids[-1] = (crit[-1] + crit[0] + 2 * math.pi) / 2
    out = set()
    for th in mids:
        o = np.argsort(P @ np.array([math.cos(th), math.sin(th)]))
        mask = 0
        out.add(0)
        for i in o[::-1]:  # the top k points labelled +
            mask |= 1 << int(i)
            out.add(mask)
    return out


def compute_growth():
    g = rng(1972)  # Sauer; Shelah, 1972
    ns = list(range(1, 17))
    half, interval = [], []
    for n in ns:
        P = g.normal(size=(n, 2))
        half.append(len(halfplane_dichotomies(P)))
        xs = np.sort(g.normal(size=n))
        sets = {0}
        for a in range(n):  # an interval [x_a, x_b] labels a contiguous run +
            for b in range(a, n):
                sets.add(sum(1 << i for i in range(a, b + 1)))
        interval.append(len(sets))
    sauer = lambda n, d: sum(math.comb(n, i) for i in range(d + 1))  # noqa: E731
    half, interval = np.array(half), np.array(interval)
    assert all(h == n * n - n + 2 for h, n in zip(half[1:], ns[1:]))  # Cover (1965): n^2 - n + 2 in general position
    assert all(v == sauer(n, 2) for v, n in zip(interval, ns))
    # a picture: 5 points and every half-plane labelling of them
    P5 = np.array([[-1.0, -0.6], [0.9, -0.8], [1.1, 0.5], [0.0, 1.0], [-1.0, 0.4]])
    l5 = sorted(halfplane_dichotomies(P5))
    vc = dict(lines_pages=vc_bound(71, 448), lines_plane=vc_bound(3, 448))
    # how many pages a linear rule on the 70 rates would need for the VC gap to fall to 0.1
    n10 = next(n for n in range(100, 10 ** 7, 50) if vc_bound(71, n) <= 0.1)
    return dict(ns=ns, half=half, interval=interval, sauer3=np.array([sauer(n, 3) for n in ns]),
                sauer2=np.array([sauer(n, 2) for n in ns]), pow2=np.array([2 ** n for n in ns]), P5=P5,
                labs5=np.array(l5), n5=len(l5), n10=n10, **vc)


# ---------------------------------------------------------------------------
def compute_rademacher():
    Ztr, ytr, _, _, _ = pages()
    g = rng(1960)
    n = len(ytr)
    ds = [1, 2, 3, 5, 8, 12, 20, 30, 45, 70]
    torch = _torch()
    torch.manual_seed(0)
    out = []
    for d in ds:
        fits = []
        for _ in range(12):
            s = g.choice([-1.0, 1.0], size=n)
            X = torch.tensor(np.c_[Ztr[:, :d], np.ones(n)], dtype=torch.float64)
            t = torch.tensor(s)
            w = torch.zeros(d + 1, dtype=torch.float64, requires_grad=True)
            opt = torch.optim.LBFGS([w], max_iter=200)

            def closure():
                opt.zero_grad()
                loss = torch.nn.functional.softplus(-t * (X @ w)).mean() + 1e-4 * (w ** 2).sum()
                loss.backward()
                return loss

            opt.step(closure)
            with torch.no_grad():
                fits.append(float(((X @ w).sign() == t).double().mean()))
        out.append(float(np.mean(fits)))
    acc = np.array(out)
    assert acc[-1] > acc[0] + 0.05
    return dict(ds=ds, acc=acc, n=n)


def compute_radlin():
    """Empirical Rademacher complexity of {x -> w.x : |w| <= 1} on the pages: E_sigma |sum_i sigma_i x_i| / n, by
    Monte Carlo over 4,000 sign vectors, against the bound sqrt(sum |x_i|^2) / n (Cauchy-Schwarz, then Jensen)."""
    Ztr, _, _, _, _ = pages()
    g = rng(2002)  # Bartlett & Mendelson, 2002
    order = g.permutation(len(Ztr))
    ns = [8, 16, 32, 64, 128, 256, 448]
    meas, sd, bound, rbound = [], [], [], []
    for n in ns:
        X = Ztr[order[:n]]
        S = g.choice([-1.0, 1.0], size=(4000, n))
        v = np.linalg.norm(S @ X, axis=1) / n
        meas.append(float(v.mean()))
        sd.append(float(v.std()))
        bound.append(float(np.sqrt((X ** 2).sum()) / n))
        rbound.append(float(np.linalg.norm(X, axis=1).max() / math.sqrt(n)))
    # the supremum is attained at w = sum sigma x / |sum sigma x|: no other direction does better
    X = Ztr
    s = g.choice([-1.0, 1.0], size=len(X))
    v = s @ X
    W = g.normal(size=(20000, X.shape[1]))
    W /= np.linalg.norm(W, axis=1, keepdims=True)
    tried = float((W @ v).max() / len(X))
    best = float(np.linalg.norm(v) / len(X))
    assert tried <= best + 1e-12 and all(m <= b + 1e-9 for m, b in zip(meas, bound))
    return dict(ns=ns, meas=np.array(meas), sd=np.array(sd), bound=np.array(bound), rbound=np.array(rbound),
                tried=tried, best=best, d=int(X.shape[1]), R=float(np.linalg.norm(Ztr, axis=1).max()))


# ---------------------------------------------------------------------------
def svm_dual(X, t, C=None, iters=20000):
    """The support vector machine without a separate bias (append a constant column for one): maximize
    sum a - 1/2 a^T Q a, 0 <= a <= C, Q = (t t^T) * (X X^T).  Returns w and the multipliers."""
    from scipy.optimize import minimize

    Q = (t[:, None] * t[None]) * (X @ X.T)
    f = lambda a: (0.5 * a @ Q @ a - a.sum(), Q @ a - 1)  # noqa: E731
    r = minimize(f, np.zeros(len(t)), jac=True, method="L-BFGS-B", bounds=[(0, C)] * len(t),
                 options=dict(maxiter=iters, maxfun=iters * 2, ftol=1e-15, gtol=1e-11))
    a = r.x
    return (a * t) @ X, a


def adaboost(X, t, Xte, tte, T=400):
    """AdaBoost with decision stumps ("x_j > theta", either sign)."""
    n, d = X.shape
    orders = np.argsort(X, 0)
    w = np.full(n, 1.0 / n)
    F, Fte = np.zeros(n), np.zeros(len(tte))
    alphas, tr_err, te_err, stumps = [], [], [], []
    for _ in range(T):
        wt = w * t
        best = (0.0, 0, 0.0, 1.0)
        for j in range(d):
            o = orders[:, j]
            xs = X[o, j]
            cum = np.concatenate([[0.0], np.cumsum(wt[o])])  # weight*label at or below each cut
            edge = wt.sum() - 2 * cum  # edge of "+1 if x > cut"
            ok = np.concatenate([[True], xs[1:] > xs[:-1], [True]])
            e = np.where(ok, edge, 0.0)
            k = int(np.argmax(np.abs(e)))
            if abs(e[k]) > abs(best[0]):
                th = xs[0] - 1 if k == 0 else (xs[-1] + 1 if k == n else 0.5 * (xs[k - 1] + xs[k]))
                best = (float(e[k]), j, float(th), float(np.sign(e[k])))
        edge, j, th, s = best
        edge = min(abs(edge), 1 - 1e-12)
        a = 0.5 * math.log((1 + edge) / (1 - edge))
        h = s * np.where(X[:, j] > th, 1.0, -1.0)
        hte = s * np.where(Xte[:, j] > th, 1.0, -1.0)
        F += a * h
        Fte += a * hte
        alphas.append(a)
        stumps.append((j, th, s))
        w = w * np.exp(-a * t * h)
        w /= w.sum()
        tr_err.append(float((np.sign(F) != t).mean()))
        te_err.append(float((np.sign(Fte) != tte).mean()))
    return np.array(tr_err), np.array(te_err), np.array(alphas), stumps


def compute_margins():
    Ztr, ytr, Zte, yte, _ = pages()
    n = len(ytr)
    t, tte = 2.0 * ytr - 1, 2.0 * yte - 1
    X, Xte = np.c_[Ztr, np.ones(n)], np.c_[Zte, np.ones(len(yte))]
    w, a = svm_dual(X, t, C=None)
    sep = bool(np.all(t * (X @ w) > 0))
    if not sep:  # not separable: the soft-margin machine
        w, a = svm_dual(X, t, C=1.0)
    R = float(np.linalg.norm(X, axis=1).max())
    m = t * (X @ w) / (np.linalg.norm(w) * R)  # normalized margins, in units of the largest |x|
    test_acc = float((np.sign(Xte @ w) == tte).mean())
    delta = 0.05
    gammas = np.round(np.geomspace(0.01, 0.5, 40), 5)
    conf = 3 * math.sqrt(math.log(2 * len(gammas) / delta) / (2 * n))  # paid once for every gamma on the grid
    emp = np.array([float((m < gm).mean()) for gm in gammas])
    cplx = 2 / (gammas * math.sqrt(n))
    bound = emp + cplx + conf
    k = int(np.argmin(bound))
    # with the same margins, how many pages would make the best bound fall below 1/2
    def best_at(m_):
        return float(np.min(emp + 2 / (gammas * math.sqrt(m_)) + 3 * math.sqrt(math.log(2 * len(gammas) / delta) / (2 * m_))))
    n_half = next(m_ for m_ in range(n, 10 ** 8, max(1, n // 4)) if best_at(m_) < 0.5)
    # AdaBoost on the same pages (Schapire, Freund, Bartlett & Lee, 1998): margins keep growing after the training
    # error reaches zero
    T = 400
    tr_err, te_err, alphas, stumps = adaboost(Ztr, t, Zte, tte, T)
    snaps = [5, 20, 100, 400]
    cdfs = {}
    for s in snaps:
        F = np.zeros(n)
        for (j, th, sg), al in zip(stumps[:s], alphas[:s]):
            F += al * sg * np.where(Ztr[:, j] > th, 1.0, -1.0)
        mm = t * F / alphas[:s].sum()
        cdfs[f"cdf{s}"] = np.sort(mm)
    zero = int(np.argmax(tr_err == 0)) + 1 if (tr_err == 0).any() else None
    return dict(sep=sep, n=n, R=R, margins=np.sort(m), test_acc=test_acc, n_sv=int((a > 1e-6 * a.max()).sum()),
                gammas=gammas, emp=emp, cplx=cplx, conf=conf, bound=bound, best_gamma=float(gammas[k]),
                best_bound=float(bound[k]), best_emp=float(emp[k]), n_half=n_half, vc=vc_bound(71, n), min_margin=float(m.min()),
                ada_tr=tr_err, ada_te=te_err, ada_T=T, ada_snaps=snaps, ada_zero=zero, **cdfs)


# ---------------------------------------------------------------------------
def compute_pacbayes():
    """A non-vacuous PAC-Bayes bound for a 70 -> 128 -> 1 network on the 448 training pages, by Dziugaite & Roy's
    recipe (2017): train the network, then optimize a Gaussian posterior N(mu, diag s^2) around it against the bound,
    with the prior N(w0, lambda I) centred at the random initialization (chosen before seeing the data), lambda
    from a grid of 256 (a union bound).  The posterior's training error is estimated from 2,000 sampled networks
    and bounded by a sample-convergence bound; the final bound inverts the binary KL (Seeger; Maurer):
        kl(err_train(Q) || err(Q)) <= (KL(Q || P) + ln(2 sqrt(n) / delta)) / n."""
    torch = _torch()
    Ztr, ytr, Zte, yte, _ = pages()
    n, d = Ztr.shape
    H = 128
    X, Xt = torch.tensor(Ztr, dtype=torch.float32), torch.tensor(Zte, dtype=torch.float32)
    t = torch.tensor(2.0 * ytr - 1, dtype=torch.float32)
    torch.manual_seed(1999)  # McAllester, 1999
    net = torch.nn.Sequential(torch.nn.Linear(d, H), torch.nn.ReLU(), torch.nn.Linear(H, 1))
    shapes = [p.shape for p in net.parameters()]
    sizes = [p.numel() for p in net.parameters()]
    w0 = torch.cat([p.detach().flatten() for p in net.parameters()]).clone()
    P = w0.numel()

    def fwd(theta, Xb):
        parts = list(torch.split(theta, sizes, dim=-1))
        if theta.dim() == 1:
            W1, b1, W2, b2 = (p.reshape(s) for p, s in zip(parts, shapes))
            return (torch.relu(Xb @ W1.T + b1) @ W2.T + b2).squeeze(-1)
        S = theta.shape[0]  # a batch of sampled networks
        W1, b1, W2, b2 = (p.reshape(S, *s) for p, s in zip(parts, shapes))
        h = torch.relu(torch.einsum("nd,shd->snh", Xb, W1) + b1[:, None, :])
        return (torch.einsum("snh,soh->sno", h, W2) + b2[:, None, :]).squeeze(-1)

    # 1. ordinary training, from w0: a short run, so the weights stay near where they started
    theta = w0.clone().requires_grad_(True)
    opt = torch.optim.SGD([theta], lr=0.01, momentum=0.9)
    sgd_curve = []
    for step in range(1, 101):
        opt.zero_grad()
        loss = torch.nn.functional.softplus(-t * fwd(theta, X)).mean()
        loss.backward()
        opt.step()
        if step % 5 == 0:
            with torch.no_grad():
                sgd_curve.append((step, float(loss), float((fwd(theta, X).sign() != t).float().mean()),
                                  float((fwd(theta, Xt).sign().numpy() != 2 * yte - 1).mean())))
    mu0 = theta.detach().clone()
    sgd_test = sgd_curve[-1][3]
    sgd_moved = float(torch.linalg.norm(mu0 - w0))
    # 2. the bound, optimized over mu, log s and log lambda
    delta, J = 0.025, 256
    grid = np.geomspace(1e-6, 1e-1, J)  # the prior variances allowed
    lam0 = 0.03
    mu = mu0.clone().requires_grad_(True)
    rho = torch.full((P,), 0.5 * math.log(lam0)).requires_grad_(True)  # log s: start as wide as the prior
    loglam = torch.tensor(math.log(lam0)).requires_grad_(True)
    steps = 10000
    opt = torch.optim.Adam([mu, rho, loglam], lr=3e-3)
    sch = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps, eta_min=1.5e-4)

    def KL(mu_, rho_, lam):
        s2 = torch.exp(2 * rho_)
        return 0.5 * ((s2 + (mu_ - w0) ** 2) / lam - 1 - torch.log(s2 / lam)).sum()

    g_ = torch.Generator().manual_seed(2017)  # Dziugaite & Roy, 2017
    const = math.log(2 * math.sqrt(n) / delta) + math.log(J)
    curve = []
    for step in range(1, steps + 1):
        opt.zero_grad()
        eps = torch.randn(P, generator=g_)
        th = mu + torch.exp(rho) * eps
        sur = torch.nn.functional.softplus(-t * fwd(th, X)).mean() / math.log(2)  # >= the 0-1 loss
        kl = KL(mu, rho, torch.exp(loglam))
        obj = sur + torch.sqrt((kl + const) / (2 * (n - 1)))
        obj.backward()
        opt.step()
        sch.step()
        if step % 100 == 0:
            with torch.no_grad():
                err = float((fwd(th, X).sign() != t).float().mean())
                curve.append((step, float(sur), float(kl), float(obj), err))
    # 3. round lambda to the grid, estimate the posterior's error, and bound it
    with torch.no_grad():
        j = int(np.argmin(np.abs(np.log(grid) - float(loglam))))
        lam = float(grid[j])
        kl = float(KL(mu, rho, torch.tensor(lam)))
        m, dp = 2000, 0.01
        errs, errs_te = [], []
        for c in range(0, m, 100):
            th = mu + torch.exp(rho) * torch.randn(100, P, generator=g_)
            errs.append((fwd(th, X).sign() != t).float().mean(1).numpy())
            errs_te.append((fwd(th, Xt).sign().numpy() != (2 * yte - 1)).mean(1))
        errs, errs_te = np.concatenate(errs), np.concatenate(errs_te)
        e_hat = float(errs.mean())
        e_up = kl_inv(e_hat, math.log(2 / dp) / m)
        bound = kl_inv(e_up, (kl + const) / n)
        mu_test = float((fwd(mu, Xt).sign().numpy() != 2 * yte - 1).mean())
        s = torch.exp(rho).numpy()
        moved = float(torch.linalg.norm(mu - w0))
    # for comparison: the same network's VC-style count, and McAllester's square-root form
    sqrt_form = e_up + math.sqrt((kl + const) / (2 * (n - 1)))
    return dict(n=n, params=int(P), H=H, kl=kl, lam=lam, e_hat=e_hat, e_up=e_up, bound=bound, sqrt_form=sqrt_form,
                test_Q=float(errs_te.mean()), test_mu=mu_test, sgd_test=sgd_test, delta=delta + dp, m=m,
                curve=np.array(curve), sgd_curve=np.array(sgd_curve), s_med=float(np.median(s)),
                s_q=np.quantile(s, [0.1, 0.9]), moved=moved, w0_norm=float(torch.linalg.norm(w0)), J=J,
                const=const, steps=steps, sgd_moved=sgd_moved)


# ---------------------------------------------------------------------------
def compute_stability():
    """Uniform stability, measured.  Ridge regression on the pages (targets +-1): swap one training page for a held-out
    one and see how far the predictions on every page move, at each ridge strength and training-set size.  Then SGD
    on logistic regression, run twice with the same order of examples on two training sets that differ in one page:
    how far apart the weights drift (Hardt, Recht & Singer, 2016)."""
    Ztr, ytr, Zte, yte, _ = pages()
    g = rng(2002)  # Bousquet & Elisseeff, 2002
    t, tte = 2.0 * ytr - 1, 2.0 * yte - 1
    Zall = np.r_[Ztr, Zte]
    n, d = Ztr.shape

    def ridge(X, y, lam):
        return np.linalg.solve(X.T @ X / len(y) + lam * np.eye(X.shape[1]), X.T @ y / len(y))

    lams = np.geomspace(1e-3, 1e2, 16)
    stab, gap = [], []
    for lam in lams:
        w = ridge(Ztr, t, lam)
        ch = []
        for _ in range(60):
            i, j = g.integers(n), g.integers(len(yte))
            X2, y2 = Ztr.copy(), t.copy()
            X2[i], y2[i] = Zte[j], tte[j]
            ch.append(float(np.abs(Zall @ (ridge(X2, y2, lam) - w)).max()))
        stab.append(float(np.mean(ch)))
        gap.append(float(((Zte @ w - tte) ** 2).mean() - ((Ztr @ w - t) ** 2).mean()))
    slope = float(np.polyfit(np.log(lams[-8:]), np.log(stab[-8:]), 1)[0])
    ns = [56, 112, 224, 448]
    lam = 1.0
    stab_n = []
    for m in ns:
        ch = []
        for _ in range(60):
            idx = g.choice(n, m, replace=False)
            X, y = Ztr[idx], t[idx]
            w = ridge(X, y, lam)
            i, j = g.integers(m), g.integers(len(yte))
            X2, y2 = X.copy(), y.copy()
            X2[i], y2[i] = Zte[j], tte[j]
            ch.append(float(np.abs(Zall @ (ridge(X2, y2, lam) - w)).max()))
        stab_n.append(float(np.mean(ch)))
    slope_n = float(np.polyfit(np.log(ns), np.log(stab_n), 1)[0])
    # SGD: same order, one page different
    eta, epochs = 0.01, 30
    G = float(np.linalg.norm(Ztr, axis=1).max())  # the logistic loss is G-Lipschitz in w on these pages
    runs = []
    for r in range(20):
        i, j = g.integers(n), g.integers(len(yte))
        X2, y2 = Ztr.copy(), t.copy()
        X2[i], y2[i] = Zte[j], tte[j]
        order = rng(100 + r).integers(0, n, size=epochs * n)
        w1, w2 = np.zeros(d), np.zeros(d)
        dist = [0.0]
        for s, k in enumerate(order, 1):
            for w, XX, yy in ((w1, Ztr, t), (w2, X2, y2)):
                z = yy[k] * (XX[k] @ w)
                w += eta * yy[k] * XX[k] / (1 + math.exp(min(z, 50)))
            if s % n == 0:
                dist.append(float(np.linalg.norm(w1 - w2)))
        runs.append(dist)
    runs = np.array(runs)
    hardt = 2 * eta * G * np.arange(epochs + 1)  # expected divergence <= 2 eta G T / n, with T = epochs * n steps
    return dict(lams=lams, stab=np.array(stab), gap=np.array(gap), slope=slope, ns=ns, stab_n=np.array(stab_n),
                slope_n=slope_n, lam_n=lam, sgd=runs, sgd_mean=runs.mean(0), hardt=hardt, eta=eta, G=G,
                epochs=epochs, n=n)


def compute_compress():
    """Littlestone & Warmuth (1986): a learner whose output is fixed by k of its n examples generalizes like a learner
    with k parameters.  The hard-margin support vector machine is one (k = its support vectors).  Bound, for a rule
    that fits all n examples: error <= (k ln n + ln(1/delta)) / (n - k)."""
    out = {}
    delta = 0.05
    pts = maxmargin_data(200, seed=1986)
    X, t = pts[:, :2], pts[:, 2]
    w, a = svm_dual(X, t)
    sv = np.nonzero(a > 1e-6 * a.max())[0]
    k = len(sv)
    out.update(X=X, t=t, w=w, sv=sv, k=k, n=len(t), bound=(k * math.log(len(t)) + math.log(1 / delta)) / (len(t) - k),
               vc=vc_bound(2, len(t)), fit=bool(np.all(t * (X @ w) > 0)))
    # retrain on the support vectors alone: the same machine
    w2, _ = svm_dual(X[sv], t[sv])
    out["same"] = float(np.linalg.norm(w2 - w) / np.linalg.norm(w))
    m = load("margins")
    Ztr, ytr, _, _, _ = pages()
    kp, n = int(m["n_sv"]), len(ytr)
    out.update(k_pages=kp, n_pages=n, sep_pages=bool(m["sep"]),
               bound_pages=min(1.0, (kp * math.log(n) + math.log(1 / delta)) / max(n - kp, 1)))
    return out


# ---------------------------------------------------------------------------
def _mlp(torch, d, widths=(512, 512)):
    layers, a = [], d
    for w in widths:
        layers += [torch.nn.Linear(a, w), torch.nn.ReLU()]
        a = w
    return torch.nn.Sequential(*layers, torch.nn.Linear(a, 2))


def compute_random():
    torch = _torch()
    Ztr, ytr, Zte, yte, _ = pages()
    torch.manual_seed(2016)  # Zhang et al. trained in 2016 (published 2017)
    g = rng(2017)
    Xtr, Xte = torch.tensor(Ztr, dtype=torch.float32), torch.tensor(Zte, dtype=torch.float32)
    out = {}
    for name, labels in (("true", ytr), ("shuffled", g.permutation(ytr))):
        torch.manual_seed(7)
        net = _mlp(torch, Ztr.shape[1])
        opt = torch.optim.Adam(net.parameters(), lr=1e-3)
        t = torch.tensor(labels, dtype=torch.long)
        curve, fits = [], []
        for step in range(1, 1501):
            opt.zero_grad()
            loss = torch.nn.functional.cross_entropy(net(Xtr), t)
            loss.backward()
            opt.step()
            if step % 10 == 0 or step < 10:
                with torch.no_grad():
                    hit = (net(Xtr).argmax(1) == t).numpy()
                    tr = float(hit.mean())
                    te = float((net(Xte).argmax(1).numpy() == yte).mean())
                curve.append((step, tr, te, float(loss)))
                fits.append(hit)
        out[name] = np.array(curve)
        # which training pages it gets right at each logged step (the order things are memorized in)
        out[f"fits_{name}"] = np.array(fits, dtype=np.uint8)
        out[f"labels_{name}"] = np.asarray(labels)
    n_params = sum(p.numel() for p in net.parameters())
    assert out["shuffled"][-1, 1] == 1.0 and abs(out["shuffled"][-1, 2] - 0.5) < 0.1 and out["true"][-1, 2] > 0.95
    first = {k: int(out[k][np.argmax(out[k][:, 1] >= 1.0), 0]) for k in ("true", "shuffled")}
    return dict(**out, n_params=int(n_params), n=len(ytr), first100=first, ytrue=np.asarray(ytr))


def compute_corrupt():
    """Zhang et al.'s sweep: a fraction f of the training labels replaced by coin flips (so about f/2 of them wrong),
    f = 0, 0.2, ..., 1, three seeds each; the same network and optimizer as `random`.  Steps until every training page
    is fit, and the accuracy on new pages then."""
    torch = _torch()
    Ztr, ytr, Zte, yte, _ = pages()
    Xtr, Xte = torch.tensor(Ztr, dtype=torch.float32), torch.tensor(Zte, dtype=torch.float32)
    fracs = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    seeds = [0, 1, 2]
    part = CACHE.partial("corrupt", dict(fracs=fracs, seeds=seeds, v=1))
    for f in fracs:
        for s in seeds:
            key = f"{f}_{s}"
            if key in part:
                continue
            g = rng(1000 + s)
            lab = ytr.copy()
            idx = g.choice(len(lab), int(round(f * len(lab))), replace=False)
            lab[idx] = g.integers(0, 2, len(idx))
            torch.manual_seed(s)
            net = _mlp(torch, Ztr.shape[1])
            opt = torch.optim.Adam(net.parameters(), lr=1e-3)
            tt = torch.tensor(lab, dtype=torch.long)
            fit_at, curve = None, []
            for step in range(1, 3001):
                opt.zero_grad()
                loss = torch.nn.functional.cross_entropy(net(Xtr), tt)
                loss.backward()
                opt.step()
                if step % 10 == 0:
                    with torch.no_grad():
                        tr = float((net(Xtr).argmax(1) == tt).float().mean())
                        te = float((net(Xte).argmax(1).numpy() == yte).mean())
                    curve.append((step, tr, te))
                    if tr == 1.0 and fit_at is None:
                        fit_at = step
                    if fit_at is not None and step >= fit_at + 100:
                        break
            part[key] = dict(fit_at=fit_at, test=curve[-1][2], wrong=float((lab != ytr).mean()), curve=curve)
    fit = np.array([[part[f"{f}_{s}"]["fit_at"] or 3000 for s in seeds] for f in fracs], float)
    test = np.array([[part[f"{f}_{s}"]["test"] for s in seeds] for f in fracs])
    wrong = np.array([[part[f"{f}_{s}"]["wrong"] for s in seeds] for f in fracs])
    curves = {f"curve{i}": np.array(part[f"{f}_0"]["curve"]) for i, f in enumerate(fracs)}
    return dict(fracs=fracs, seeds=seeds, fit=fit, test=test, wrong=wrong, **curves)


# ---------------------------------------------------------------------------
def compute_minnorm():
    """Gradient descent on least squares with more unknowns (d = 60) than equations (n = 20), from zero: the iterates
    never leave the row space, and converge to the pseudoinverse solution.  From another start, to a different
    interpolant.  And a three-dimensional picture: n = 2 equations in d = 3 unknowns."""
    g = rng(1955)  # Penrose's pseudoinverse, 1955
    n, d = 20, 60
    X = g.normal(size=(n, d))
    y = g.normal(size=n)
    wp = np.linalg.pinv(X) @ y
    L = np.linalg.eigvalsh(X.T @ X / n).max()
    eta = 1.0 / L
    P = np.linalg.pinv(X) @ X  # projector onto the row space
    out = {}
    w_other = g.normal(size=d)
    for name, w0 in (("zero", np.zeros(d)), ("other", w_other)):
        w = w0.copy()
        dist, res, null = [], [], []
        ts = np.unique(np.round(np.geomspace(1, 20000, 120)).astype(int))
        k = 0
        for s in range(1, 20001):
            w -= eta * X.T @ (X @ w - y) / n
            if k < len(ts) and s == ts[k]:
                dist.append(float(np.linalg.norm(w - wp)))
                res.append(float(np.linalg.norm(X @ w - y)))
                null.append(float(np.linalg.norm(w - P @ w)))
                k += 1
        out[name] = dict(dist=np.array(dist), res=np.array(res), null=np.array(null), norm=float(np.linalg.norm(w)))
        out["ts"] = ts
    # from w0 the limit is w+ + (I - P) w0: the start's null-space part never moves
    pred = wp + (np.eye(d) - P) @ w_other
    # three dimensions: two equations; the solutions form a line, GD from 0 lands at its closest point to 0
    X3 = np.array([[1.0, 0.4, 0.2], [0.1, 0.9, 0.5]])
    y3 = np.array([1.2, 0.8])
    w3p = np.linalg.pinv(X3) @ y3
    null3 = np.linalg.svd(X3)[2][-1]
    w = np.zeros(3)
    path = [w.copy()]
    eta3 = 0.6 / np.linalg.eigvalsh(X3.T @ X3).max()
    for _ in range(60):
        w = w - eta3 * X3.T @ (X3 @ w - y3)
        path.append(w.copy())
    return dict(n=n, d=d, ts=out["ts"], dist0=out["zero"]["dist"], res0=out["zero"]["res"], null0=out["zero"]["null"],
                dist1=out["other"]["dist"], res1=out["other"]["res"], norm_pinv=float(np.linalg.norm(wp)),
                norm0=out["zero"]["norm"], norm1=out["other"]["norm"], pred_gap=float(np.linalg.norm(pred - wp)),
                X3=X3, y3=y3, w3p=w3p, null3=null3, path3=np.array(path), eta=eta)


def maxmargin_data(n=40, seed=2018):
    """Two clouds on either side of a line through the origin, plus four points near it (two per class) that set the
    widest margin: the clouds pull the early direction one way, the four points decide the final one."""
    g = rng(seed)
    pts = []
    for i in range(n - 4):
        s = 1.0 if i % 2 == 0 else -1.0
        pts.append([*(s * np.array([1.7, 1.3]) + g.normal(0, 0.38, 2)), s])
    for s in (1.0, -1.0):
        for _ in range(2):
            pts.append([*(s * (np.array([1.25, -0.45]) + g.normal(0, 0.08, 2))), s])
    return np.array(pts)


def compute_maxmargin():
    """Soudry, Hoffer, Nacson, Gunasekar & Srebro (2018): on separable data, gradient descent on the logistic loss
    sends |w| to infinity like log t, and its direction to the max-margin (hard SVM) direction, the angle shrinking
    like 1/log t.  Two dimensions, no bias, a million steps."""
    pts = maxmargin_data()
    X, t = pts[:, :2], pts[:, 2]
    ths = np.linspace(0, 2 * math.pi, 200001)
    U = np.stack([np.cos(ths), np.sin(ths)], 1)
    mar = (t[:, None] * (X @ U.T)).min(0)
    th_svm = float(ths[int(np.argmax(mar))])
    w_svm = np.array([math.cos(th_svm), math.sin(th_svm)])
    gamma = float(mar.max())
    w_dual, _ = svm_dual(X, t)
    assert abs(math.atan2(w_dual[1], w_dual[0]) - math.atan2(w_svm[1], w_svm[0])) < 1e-3
    n = len(t)
    L = 0.25 * float(np.linalg.eigvalsh(X.T @ X / n).max())
    eta = 1.0 / L
    w = np.zeros(2)
    T = 1_000_000
    logs = set(np.unique(np.round(np.geomspace(1, T, 160)).astype(int)).tolist())
    rec = []
    tX = t[:, None] * X
    for s in range(1, T + 1):
        z = tX @ w
        w = w + eta * (tX.T @ (0.5 * (1 - np.tanh(0.5 * z)))) / n  # -grad of mean log(1 + e^{-z})
        if s in logs:
            ang = math.degrees(math.acos(min(1.0, float(w @ w_svm / np.linalg.norm(w)))))
            loss = float(np.logaddexp(0, -z).mean())
            rec.append((s, ang, float(np.linalg.norm(w)), loss, float((tX @ w).min() / np.linalg.norm(w)), *w))
    rec = np.array(rec)
    # angle times log t: roughly constant if the rate is 1/log t
    late = rec[rec[:, 0] >= 1000]
    c = late[:, 1] * np.log(late[:, 0])
    return dict(X=X, t=t, w_svm=w_svm, gamma=gamma, rec=rec, eta=eta, T=T, c_lo=float(c.min()), c_hi=float(c.max()),
                angle_end=float(rec[-1, 1]), norm_end=float(rec[-1, 2]), margin_end=float(rec[-1, 4]))


# ---------------------------------------------------------------------------
def rf_features(Z, W):
    return np.maximum(Z @ W, 0)


def compute_double():
    Ztr, ytr, Zte, yte, _ = pages()
    g = rng(2019)  # Belkin, Hsu, Ma & Mandal, 2019
    n, d = Ztr.shape
    ps = np.unique(np.round(np.logspace(np.log10(10), np.log10(6000), 46)).astype(int))
    ps = np.unique(np.concatenate([ps, [n - 8, n, n + 8]]))
    ttr, tte = 2.0 * ytr - 1, 2.0 * yte - 1
    lams = [1e-2, 1.0, 1e2]
    errs, tr_errs, norms, smin, ridge = [], [], [], [], []
    spectra = {}
    show = [100, 250, 400, n - 8, n, n + 8, 600, 1000, 3000]
    reps = 5
    for p in ps:
        e, et, nm, sm, rr = [], [], [], [], []
        for r in range(reps):
            W = g.normal(size=(d, p)) / math.sqrt(d)
            Ftr, Fte = rf_features(Ztr, W), rf_features(Zte, W)
            U, S, Vt = np.linalg.svd(Ftr, full_matrices=False)
            keep = S > S[0] * 1e-12
            beta = Vt[keep].T @ ((U[:, keep].T @ ttr) / S[keep])  # the pseudoinverse solution
            e.append(float(((Fte @ beta - tte) ** 2).mean()))
            et.append(float(((Ftr @ beta - ttr) ** 2).mean()))
            nm.append(float(np.linalg.norm(beta)))
            sm.append(float(S[keep].min() / math.sqrt(p)))
            uy = U.T @ ttr
            rr.append([float(((Fte @ (Vt.T @ (S * uy / (S ** 2 + lam * p))) - tte) ** 2).mean()) for lam in lams])
            if r == 0 and int(p) in show:
                spectra[f"spec{int(p)}"] = S / math.sqrt(p)
        errs.append(np.median(e))
        tr_errs.append(np.median(et))
        norms.append(np.median(nm))
        smin.append(np.median(sm))
        ridge.append(np.median(np.array(rr), 0))
    errs, tr_errs = np.array(errs), np.array(tr_errs)
    k_n = int(np.argmin(np.abs(ps - n)))
    assert errs[k_n] > 3 * errs[0] and errs[-1] < errs[k_n] / 3 and tr_errs[-1] < 1e-6
    return dict(ps=ps, test=errs, train=tr_errs, norms=np.array(norms), smin=np.array(smin), ridge=np.array(ridge),
                lams=lams, n=n, d=d, peak=float(errs[k_n]), show=[s for s in show if f"spec{s}" in spectra],
                **spectra)


def compute_samplewise():
    """Fix p = 200 random features; train on n = 20 ... 448 of the training pages (20 random subsets each)."""
    Ztr, ytr, Zte, yte, _ = pages()
    g = rng(2020)  # Nakkiran et al., Deep Double Descent (ICLR 2020)
    d = Ztr.shape[1]
    p = 200
    W = g.normal(size=(d, p)) / math.sqrt(d)
    Ftr, Fte = rf_features(Ztr, W), rf_features(Zte, W)
    ttr, tte = 2.0 * ytr - 1, 2.0 * yte - 1
    ns = np.unique(np.concatenate([np.round(np.geomspace(20, 448, 28)).astype(int), [180, 190, 200, 210, 220]]))
    med, lo, hi, rid = [], [], [], []
    for m in ns:
        e, er = [], []
        for _ in range(20):
            idx = g.choice(len(ttr), m, replace=False)
            beta = np.linalg.pinv(Ftr[idx]) @ ttr[idx]
            e.append(float(((Fte @ beta - tte) ** 2).mean()))
            br = np.linalg.solve(Ftr[idx].T @ Ftr[idx] + 1.0 * p * np.eye(p), Ftr[idx].T @ ttr[idx])
            er.append(float(((Fte @ br - tte) ** 2).mean()))
        med.append(np.median(e))
        lo.append(np.quantile(e, 0.25))
        hi.append(np.quantile(e, 0.75))
        rid.append(np.median(er))
    med = np.array(med)
    k = int(np.argmax(med))
    return dict(p=p, ns=ns, med=med, lo=np.array(lo), hi=np.array(hi), ridge=np.array(rid), peak_n=int(ns[k]),
                worse=bool(med[k] > med[0]))


def compute_epochwise():
    """Gradient descent from zero on a linear regression whose inputs have two scales (Heckel & Yilmaz, 2021): 150
    directions of variance 1 holding a little of the signal, learned fast; 5 of variance 0.0003 holding the rest,
    learned thousands of times more slowly.  n = 200 examples.  The exact test error at every step (from the eigen-
    decomposition), split into the two groups' shares; medians over 20 draws of the data."""
    g = rng(2021)
    n, d1, d2, sig, s1, s2, l2 = 200, 150, 5, 0.3, 4.0, 3.0, 3e-4
    lam = np.r_[np.ones(d1), np.full(d2, l2)]  # input variances
    ws = np.r_[g.normal(0, math.sqrt(s1 / d1), d1), g.normal(0, math.sqrt(s2 / d2 / l2), d2)]
    ts = np.unique(np.round(np.geomspace(1, 3e6, 200)).astype(int))
    curves, fast, slow, tr_curves = [], [], [], []
    for r in range(20):
        X = g.normal(size=(n, d1 + d2)) * np.sqrt(lam)
        y = X @ ws + sig * g.normal(size=n)
        A = X.T @ X / n
        ev, V = np.linalg.eigh(A)
        eta = 1.0 / ev.max()
        b = V.T @ (X.T @ y / n)
        # w_t = V diag((1 - (1 - eta ev)^t) / ev) b, exactly
        dec = (1 - eta * ev)[None, :] ** ts[:, None]
        coef = (1 - dec) / ev
        Wt = (coef * b) @ V.T
        E2 = (Wt - ws) ** 2 * lam
        fast.append(E2[:, :d1].sum(1))
        slow.append(E2[:, d1:].sum(1))
        curves.append(E2.sum(1) + sig ** 2)
        tr_curves.append(((X @ Wt.T - y[:, None]) ** 2).mean(0))
    C = np.array(curves)
    med = np.median(C, 0)
    i1 = int(np.argmin(med[: np.searchsorted(ts, 100)]))
    i2 = i1 + int(np.argmax(med[i1:np.searchsorted(ts, 1e4)]))
    double = bool(med[i2] > med[i1] * 1.05 and med[-1] < med[i2] * 0.95)
    return dict(ts=ts, med=med, lo=np.quantile(C, 0.25, 0), hi=np.quantile(C, 0.75, 0), fast=np.median(fast, 0),
                slow=np.median(slow, 0), train=np.median(np.array(tr_curves), 0), noise=sig ** 2, i1=i1, i2=i2,
                double=double, n=n, d1=d1, d2=d2, start=float(s1 + s2 + sig ** 2))


def compute_benign():
    """Bartlett, Long, Lugosi & Tsigler (2020).  n = 100 noisy examples; the signal lives in 5 strong directions.  The
    minimum-norm interpolant fits every noisy label exactly.  With a spike plus D weak directions of total variance 5,
    its excess error falls toward zero as D grows (benign); with D more directions as strong as the signal's, it does
    not."""
    g = rng(2020)
    n, s, sig, tail = 100, 5, 0.5, 5.0
    Ds = [100, 200, 400, 1000, 2000, 5000, 10000, 20000, 40000]
    ws = np.zeros(s)
    ws[:] = 1.0
    out_b, out_i, out_bs, out_is, tr = [], [], [], [], []
    for D in Ds:
        eb, ei = [], []
        for r in range(12):
            for kind in ("spiked", "iso"):
                lam = np.r_[np.ones(s), np.full(D, tail / D if kind == "spiked" else 1.0)]
                X = g.normal(size=(n, s + D)) * np.sqrt(lam)
                y = X[:, :s] @ ws + sig * g.normal(size=n)
                w = X.T @ np.linalg.solve(X @ X.T, y)
                e = w.copy()
                e[:s] -= ws
                ex = float((e ** 2 * lam).sum())
                (eb if kind == "spiked" else ei).append(ex)
                if kind == "spiked":
                    tr.append(float(np.abs(X @ w - y).max()))
        out_b.append(np.median(eb))
        out_i.append(np.median(ei))
        out_bs.append(np.quantile(eb, [0.25, 0.75]))
        out_is.append(np.quantile(ei, [0.25, 0.75]))
    # a one-dimensional picture of a benign fit: the spike direction, and the tail's spikes at the training points
    return dict(Ds=Ds, n=n, s=s, sig=sig, noise=sig ** 2, tail=tail, spiked=np.array(out_b), iso=np.array(out_i),
                spiked_q=np.array(out_bs), iso_q=np.array(out_is), max_train=float(max(tr)))


# ---------------------------------------------------------------------------
def _teacher_data(n, seed):
    g = rng(seed)
    Wt = g.normal(size=(10, 6))
    vt = g.normal(size=6)

    def f(X):
        return np.tanh(X @ Wt) @ vt

    X = g.normal(size=(n, 10))
    Xte = g.normal(size=(4000, 10))
    return X, (f(X) > 0).astype(np.int64), Xte, (f(Xte) > 0).astype(np.int64)


def _top_eig(torch, net, X, t, iters=40, seed=0):
    params = [p for p in net.parameters()]
    loss = torch.nn.functional.cross_entropy(net(X), t)
    grads = torch.autograd.grad(loss, params, create_graph=True)
    gen = torch.Generator().manual_seed(seed)
    v = [torch.randn(p.shape, generator=gen) for p in params]
    nv = torch.sqrt(sum((a * a).sum() for a in v))
    v = [a / nv for a in v]
    lam = 0.0
    for _ in range(iters):
        Hv = torch.autograd.grad(grads, params, grad_outputs=v, retain_graph=True)
        lam = float(sum((a * b).sum() for a, b in zip(Hv, v)))
        nv = torch.sqrt(sum((a * a).sum() for a in Hv))
        v = [a / nv for a in Hv]
    return lam


def compute_sharp():
    """Keskar et al. (2017) and Dinh et al. (2017), small.  A teacher network labels points in 10 dimensions; students
    (10 -> 256 -> 2, ReLU) learn from 300 of them with SGD at batch sizes 4 ... 300 and two step sizes, three seeds each,
    each until its training loss falls below 0.01 (so all are compared at the same fit).  Sharpness: the top eigenvalue of the training loss's Hessian; and the loss rise under random
    weight perturbations.  Then one trained network rescaled (first layer times a, second divided by a): the same
    function, a different sharpness."""
    torch = _torch()
    X, y, Xte, yte = _teacher_data(300, 1997)  # Hochreiter & Schmidhuber, Flat Minima (1997)
    Xt, yt = torch.tensor(X, dtype=torch.float32), torch.tensor(y)
    Xv = torch.tensor(Xte, dtype=torch.float32)
    batches = [4, 16, 64, 300]
    lrs = [0.02, 0.1]
    seeds = [0, 1, 2]
    TARGET = 0.01
    part = CACHE.partial("sharp", dict(b=batches, lr=lrs, s=seeds, v=3, target=TARGET))
    for B in batches:
        for lr in lrs:
            for s in seeds:
                key = f"{B}_{lr}_{s}"
                if key in part:
                    continue
                torch.manual_seed(s)
                net = torch.nn.Sequential(torch.nn.Linear(10, 256), torch.nn.ReLU(), torch.nn.Linear(256, 2))
                opt = torch.optim.SGD(net.parameters(), lr=lr)
                gen = torch.Generator().manual_seed(100 + s)
                ep = 0
                while ep < 4000:  # until the training loss falls to the common target
                    perm = torch.randperm(len(yt), generator=gen)
                    for i in range(0, len(yt), B):
                        idx = perm[i:i + B]
                        opt.zero_grad()
                        torch.nn.functional.cross_entropy(net(Xt[idx]), yt[idx]).backward()
                        opt.step()
                    ep += 1
                    with torch.no_grad():
                        if float(torch.nn.functional.cross_entropy(net(Xt), yt)) < TARGET:
                            break
                with torch.no_grad():
                    tr_loss = float(torch.nn.functional.cross_entropy(net(Xt), yt))
                    tr_acc = float((net(Xt).argmax(1) == yt).float().mean())
                    te_err = float((net(Xv).argmax(1).numpy() != yte).mean())
                lam = _top_eig(torch, net, Xt, yt, seed=s)
                # average loss rise under Gaussian weight noise of relative size 0.05 (a "flatness" measure)
                with torch.no_grad():
                    base = [p.clone() for p in net.parameters()]
                    rises = []
                    pg = torch.Generator().manual_seed(7)
                    for _ in range(20):
                        for p, b0 in zip(net.parameters(), base):
                            p.copy_(b0 + 0.05 * b0.abs().mean() * torch.randn(p.shape, generator=pg))
                        rises.append(float(torch.nn.functional.cross_entropy(net(Xt), yt)) - tr_loss)
                    for p, b0 in zip(net.parameters(), base):
                        p.copy_(b0)
                part[key] = dict(B=B, lr=lr, s=s, tr_loss=tr_loss, tr_acc=tr_acc, te_err=te_err, lam=lam,
                                 rise=float(np.mean(rises)), epochs=ep)
                if B == 300 and lr == 0.1 and s == 0:
                    torch.save(net.state_dict(), CACHE.dir / "sharp_net.pt")
    rows = [part[f"{B}_{lr}_{s}"] for B in batches for lr in lrs for s in seeds]
    lam = np.array([r["lam"] for r in rows])
    err = np.array([r["te_err"] for r in rows])
    rise = np.array([r["rise"] for r in rows])
    from scipy.stats import spearmanr

    rho = float(spearmanr(lam, err).statistic)
    rho_rise = float(spearmanr(rise, err).statistic)
    # rescaling: (W1, b1) * a, W2 / a.  ReLU(a z) = a ReLU(z), so the function is unchanged
    net = torch.nn.Sequential(torch.nn.Linear(10, 256), torch.nn.ReLU(), torch.nn.Linear(256, 2))
    net.load_state_dict(torch.load(CACHE.dir / "sharp_net.pt"))
    alphas = [0.25, 0.5, 1.0, 2.0, 4.0]
    resc, same = [], []
    with torch.no_grad():
        ref = net(Xv).clone()
    for a in alphas:
        m = torch.nn.Sequential(torch.nn.Linear(10, 256), torch.nn.ReLU(), torch.nn.Linear(256, 2))
        m.load_state_dict(net.state_dict())
        with torch.no_grad():
            m[0].weight *= a
            m[0].bias *= a
            m[2].weight /= a
        resc.append(_top_eig(torch, m, Xt, yt, iters=60))
        with torch.no_grad():
            same.append(float((m(Xv) - ref).abs().max()))
    return dict(batches=batches, lrs=lrs, seeds=seeds, B=np.array([r["B"] for r in rows]),
                lr=np.array([r["lr"] for r in rows]), lam=lam, err=err, rise=rise,
                tr_acc=np.array([r["tr_acc"] for r in rows]), tr_loss=np.array([r["tr_loss"] for r in rows]),
                epochs=np.array([r["epochs"] for r in rows]), target=TARGET, rho=rho, rho_rise=rho_rise, alphas=alphas,
                resc=np.array(resc), same=float(max(same)), n=300)


# ---------------------------------------------------------------------------
SHIFT = dict(mu_tr=0.5, sd_tr=0.5, mu_te=0.0, sd_te=0.3, noise=0.3)  # after Shimodaira (2000)


def shift_f(x):
    return -x + x ** 3


def compute_shift():
    """Covariate shift: training inputs ~ N(0.5, 0.5^2), test inputs ~ N(0, 0.3^2), y = -x + x^3 + noise, and a
    straight line to fit (the model is wrong, so where the inputs fall matters).  Least squares; least squares weighted
    by w(x) = q(x)/p(x), exact; flattened, w^0.5; and with w estimated by a logistic classifier told apart training
    inputs from 100 unlabelled test inputs.  1,000 draws of n = 100."""
    from scipy.stats import norm

    S = SHIFT
    g = rng(2000)  # Shimodaira, 2000
    n, runs = 100, 1000

    def wts(x):
        return norm.pdf(x, S["mu_te"], S["sd_te"]) / norm.pdf(x, S["mu_tr"], S["sd_tr"])

    def fit(x, y, w):
        A = np.c_[np.ones_like(x), x]
        return np.linalg.solve(A.T @ (A * w[:, None]), A.T @ (w * y))

    xt = g.normal(S["mu_te"], S["sd_te"], 20000)
    yt = shift_f(xt)

    def risk(c):
        return float(((c[0] + c[1] * xt - yt) ** 2).mean() + S["noise"] ** 2)

    res = {k: [] for k in ("ols", "iw", "flat", "est")}
    ess, coefs = [], {k: [] for k in res}
    for r in range(runs):
        x = g.normal(S["mu_tr"], S["sd_tr"], n)
        y = shift_f(x) + S["noise"] * g.normal(size=n)
        u = g.normal(S["mu_te"], S["sd_te"], 100)  # unlabelled test inputs
        w = wts(x)
        # logistic regression on (x, x^2): test (1) against training (0); w = odds * n_train / n_test
        Z = np.r_[x, u]
        lab = np.r_[np.zeros(n), np.ones(100)]
        F = np.c_[np.ones_like(Z), Z, Z ** 2]
        beta = np.zeros(3)
        for _ in range(30):  # Newton
            p = 1 / (1 + np.exp(-F @ beta))
            Hs = F.T @ (F * (p * (1 - p))[:, None]) + 1e-6 * np.eye(3)
            beta += np.linalg.solve(Hs, F.T @ (lab - p))
        west = np.exp(np.c_[np.ones_like(x), x, x ** 2] @ beta) * n / 100
        for k, ww in (("ols", np.ones(n)), ("iw", w), ("flat", np.sqrt(w)), ("est", west)):
            c = fit(x, y, ww)
            res[k].append(risk(c))
            coefs[k].append(c)
        ess.append(float(w.sum() ** 2 / (w ** 2).sum()))
    out = {k: np.array(v) for k, v in res.items()}
    best_line = np.polyfit(xt, yt, 1)[::-1]
    g2 = rng(1)
    x0 = g2.normal(S["mu_tr"], S["sd_tr"], n)
    y0 = shift_f(x0) + S["noise"] * g2.normal(size=n)
    return dict(n=n, runs=runs, **{f"{k}_mean": float(v.mean()) for k, v in out.items()},
                **{f"{k}_se": float(v.std() / math.sqrt(runs)) for k, v in out.items()},
                **{f"{k}_coef": np.median(np.array(c), 0) for k, c in coefs.items()},
                ess_mean=float(np.mean(ess)), best_risk=risk(best_line), noise_var=S["noise"] ** 2,
                x0=x0, y0=y0, w0=wts(x0), **S)


# ---------------------------------------------------------------------------
def compute_memorize():
    """Carlini et al.'s test of memorization (2023), on the series' novels model (6 million weights, trained on 6.6
    million tokens of thirty novels): a training passage of 64 tokens is "extractable" if, given its first 32 tokens,
    greedy decoding reproduces the next 32 exactly.  Greedy decoding reproduces them exactly when, at every one of the
    32 positions, the model's top token given the true text so far is the true next token, so one forward pass decides
    it.  Passages sampled by how many times they occur in the training text, and held-out passages for comparison."""
    torch = _torch()
    from explainer.ai.novels import decode, load_base, token_arrays

    train, valid = token_arrays()
    tr = train.astype(np.uint64)
    L, half = 64, 32
    B = np.uint64(1_000_003)
    # rolling hash of every 64-token window (wrapping uint64 arithmetic)
    with np.errstate(over="ignore"):
        pw = np.ones(L, np.uint64)
        for i in range(1, L):
            pw[i] = pw[i - 1] * B
        h = np.zeros(len(tr) - L + 1, np.uint64)
        for j in range(L):
            h = h * B + tr[j:len(tr) - L + 1 + j]
    uniq, inv, counts = np.unique(h, return_inverse=True, return_counts=True)
    cnt = counts[inv]  # how often each window's passage occurs
    g = rng(2021)  # Carlini et al., 2021
    bins = [(1, 1), (2, 2), (3, 4), (5, 8), (9, 16), (17, 10 ** 9)]
    per = 300
    model = load_base()
    picked = {}
    for lo, hi in bins:
        idx = np.nonzero((cnt >= lo) & (cnt <= hi))[0]
        # one window per distinct passage
        _, first = np.unique(h[idx], return_index=True)
        idx = idx[first]
        picked[(lo, hi)] = g.choice(idx, min(per, len(idx)), replace=False) if len(idx) else np.array([], int)
    vstart = g.choice(len(valid) - L, per, replace=False)

    def score(seqs, ctx):
        """For each 64-token passage: exact (all 32 continuation tokens are the greedy choices) and how many of the 32
        are matched before the first miss, given the last `ctx` tokens of the first half as the prompt."""
        ex, run = [], []
        for i in range(0, len(seqs), 50):
            S = torch.tensor(np.array(seqs[i:i + 50]).astype(np.int64))[:, half - ctx:]
            with torch.no_grad():
                pred = model(S[:, :-1]).argmax(-1)[:, ctx - 1:]
            hit = (pred == S[:, ctx:]).numpy()
            ex += hit.all(1).tolist()
            run += [int(np.argmin(np.r_[r, False])) for r in hit]
        return np.array(ex), np.array(run)

    rows = []
    examples = []
    for (lo, hi), idx in picked.items():
        seqs = [train[i:i + L] for i in idx]
        res = {}
        for ctx in (8, 32):
            e, r = score(seqs, ctx) if seqs else (np.array([]), np.array([]))
            res[ctx] = (float(e.mean()) if len(e) else float("nan"), float(r.mean()) if len(r) else float("nan"))
        rows.append(dict(lo=lo, hi=hi, k=len(idx), exact32=res[32][0], run32=res[32][1], exact8=res[8][0],
                         run8=res[8][1], med_count=float(np.median(cnt[idx])) if len(idx) else float("nan")))
        e, _ = score(seqs, 32)
        for j in np.nonzero(e)[0][:2]:
            examples.append(dict(count=int(cnt[idx[j]]), prefix=decode(seqs[j][:half]), suffix=decode(seqs[j][half:])))
    vseqs = [valid[i:i + L] for i in vstart]
    ve, vr = score(vseqs, 32)
    ve8, vr8 = score(vseqs, 8)
    # a passage seen once, for the picture: what the model says instead
    once = picked[(1, 1)]
    seqs = [train[i:i + L] for i in once[:50]]
    e, r = score(seqs, 32)
    j = int(np.argmax(r * (~e)))  # the longest partial match that is not exact
    S = torch.tensor(np.array(seqs[j]).astype(np.int64))[None]
    with torch.no_grad():
        ids = S[0, :half].tolist()
        for _ in range(half):
            ids.append(int(model(torch.tensor([ids]))[0, -1].argmax()))
    miss = dict(prefix=decode(seqs[j][:half]), truth=decode(seqs[j][half:]), model=decode(ids[half:]), run=int(r[j]))
    dup_share = float((counts > 1).sum() / len(counts))
    return dict(rows=rows, valid_exact32=float(ve.mean()), valid_run32=float(vr.mean()), valid_exact8=float(ve8.mean()),
                valid_run8=float(vr8.mean()), examples=examples[:6], miss=miss, n_windows=int(len(h)),
                n_distinct=int(len(uniq)), dup_share=dup_share, train_tokens=int(len(train)), per=per,
                max_count=int(counts.max()))


CANARY = dict(counts=[1, 2, 4, 8, 16, 32, 64], per=16, L=64, filler=250_000, lr=1e-3, batch=16, passes=3.0, evals=12)


def compute_canary():
    """Kandpal, Wallace & Raffel (2022) and Carlini et al. (2023), on our model.  Continue training the novels model on
    250,000 tokens of its own training text, into which 112 passages of 64 tokens from the held-out text, never seen
    before, are planted: 16 passages once, 16 twice, ... 16 sixty-four times; three passes.  Sixteen more held-out passages are never
    planted (the control).  Every few steps: how many of each group are extractable (their last 32 tokens are the
    greedy continuation of their first 32).  Checkpointed, so a killed run resumes."""
    torch = _torch()
    torch.set_num_threads(int(os.environ.get("AI8_TRAIN_THREADS", "2")))
    from explainer.ai.novels import decode, load_base, token_arrays

    K = CANARY
    train, valid = token_arrays()
    g = rng(2022)  # Kandpal, Wallace & Raffel, 2022
    L, half = K["L"], K["L"] // 2
    groups = K["counts"] + [0]
    starts = g.choice(len(valid) // L, K["per"] * len(groups), replace=False) * L  # disjoint passages
    passages = np.array([valid[s:s + L] for s in starts]).astype(np.int64).reshape(len(groups), K["per"], L)
    a0 = int(g.integers(0, len(train) - K["filler"]))
    filler = train[a0:a0 + K["filler"]]
    pieces = [passages[i, j] for i, c in enumerate(groups) for j in range(K["per"]) for _ in range(c)]
    order = g.permutation(len(pieces))
    cuts = np.sort(g.choice(len(filler), len(pieces), replace=False))
    out, prev = [], 0
    for c, k in zip(cuts, order):
        out += [filler[prev:c], pieces[k]]
        prev = c
    out.append(filler[prev:])
    arr = np.concatenate(out).astype(np.int64)
    seq = 256
    steps = int(math.ceil(K["passes"] * len(arr) / (K["batch"] * seq)))
    every = max(1, steps // K["evals"])
    ck = CACHE.dir / "canary.ckpt"
    model = load_base()
    model.train()
    opt = torch.optim.AdamW(model.parameters(), lr=K["lr"], weight_decay=0.0)
    data_rng = rng(7)
    curve, evals, step = [], [], 0
    if ck.exists():
        st = torch.load(ck, weights_only=False)
        model.load_state_dict(st["model"])
        opt.load_state_dict(st["opt"])
        data_rng.bit_generator.state = st["data_rng"]
        curve, evals, step = st["curve"], st["evals"], st["step"]
        print(f"  resuming canary at step {step}/{steps}", flush=True)

    P = torch.tensor(passages.reshape(-1, L))

    def extract():
        model.eval()
        with torch.no_grad():
            pred = model(P[:, :-1]).argmax(-1)[:, half - 1:]
        model.train()
        hit = (pred == P[:, half:]).numpy().reshape(len(groups), K["per"], half)
        exact = hit.all(2).mean(1)
        run = np.array([[int(np.argmin(np.r_[r, False])) for r in grp] for grp in hit]).mean(1)
        return exact.tolist(), run.tolist()

    if not evals:
        evals.append([0, *extract()])
    t0 = time.time()
    while step < steps:
        ix = data_rng.integers(0, len(arr) - seq - 1, K["batch"])
        x = torch.tensor(np.stack([arr[i:i + seq + 1] for i in ix]))
        lr = K["lr"] * min(1.0, (step + 1) / 10)
        for gr in opt.param_groups:
            gr["lr"] = lr
        loss = torch.nn.functional.cross_entropy(model(x[:, :-1]).flatten(0, 1), x[:, 1:].flatten())
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        step += 1
        curve.append([step, float(loss)])
        if step % every == 0 or step == steps:
            evals.append([step, *extract()])
            tmp = ck.with_suffix(".tmp")
            torch.save(dict(model=model.state_dict(), opt=opt.state_dict(), data_rng=data_rng.bit_generator.state,
                            curve=curve, evals=evals, step=step), tmp)
            tmp.replace(ck)
            print(f"  canary step {step}/{steps}  loss {loss.item():.3f}  exact {np.round(evals[-1][1], 2)}  "
                  f"{(time.time() - t0) / max(1, len(curve)):.1f}s/step", flush=True)
    # one planted passage, shown: the most-repeated group's first extractable one, and a once-seen one's attempt
    model.eval()
    shown = {}
    with torch.no_grad():
        for gi in (len(groups) - 2, 0):
            j = 0
            ids = passages[gi, j, :half].tolist()
            for _ in range(half):
                ids.append(int(model(torch.tensor([ids]))[0, -1].argmax()))
            shown[f"g{gi}"] = dict(count=groups[gi], prefix=decode(passages[gi, j, :half]),
                                   truth=decode(passages[gi, j, half:]), model=decode(ids[half:]))
    ex = np.array([e[1] for e in evals])
    rn = np.array([e[2] for e in evals])
    res = dict(groups=groups, steps=steps, every=every, eval_steps=[e[0] for e in evals], exact=ex, run=rn,
               curve=np.array(curve), arr_tokens=int(len(arr)), planted_tokens=int(sum(len(p) for p in pieces)),
               shown=shown, **K)
    ck.unlink(missing_ok=True)
    return res


ITEMS = {
    "gap": compute_gap,
    "risk": compute_risk,
    "biasvar": compute_biasvar,
    "hoeffding": compute_hoeffding,
    "union": compute_union,
    "shatter": compute_shatter,
    "growth": compute_growth,
    "rademacher": compute_rademacher,
    "radlin": compute_radlin,
    "margins": compute_margins,
    "pacbayes": compute_pacbayes,
    "stability": compute_stability,
    "compress": compute_compress,
    "random": compute_random,
    "corrupt": compute_corrupt,
    "minnorm": compute_minnorm,
    "maxmargin": compute_maxmargin,
    "double": compute_double,
    "samplewise": compute_samplewise,
    "epochwise": compute_epochwise,
    "benign": compute_benign,
    "sharp": compute_sharp,
    "shift": compute_shift,
    "memorize": compute_memorize,
    "canary": compute_canary,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
