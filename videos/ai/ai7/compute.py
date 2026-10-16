"""Precompute everything numerical in Part 7 of the AI series ("Fitting and Generalizing").

    python -m videos.ai.ai7.compute              # everything missing (needs Part 5's pages: .cache/ai5)
    python -m videos.ai.ai7.compute --force double

Results are cached in ``.cache/ai7/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

Items:
    gap       the training error and the test error of Part 5's k-nearest-neighbour vote, k = 1 ... 151
    biasvar   bias and variance by resampling: polynomials of degree 0 ... 15 fitted to 200 fresh samples of 16 noisy
              points from one curve (illustrative); bias squared + variance + noise = the expected test error
    shatter   lines in the plane: all 8 labellings of 3 points are separable, 2 of the 16 labellings of 4 are not
    rademacher how well linear classifiers on the first d of Part 5's 70 rates can fit random signs, d = 1 ... 70
    random    one network (70 -> 512 -> 512 -> 2) trained on Part 5's pages with the true authors and with shuffled
              authors: training and test accuracy through training
    double    double descent: least squares on p random features of Part 5's pages (minimum-norm when p > n), test
              error against p, peaking where p = n
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai7")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def pages():
    from videos.ai.ai5 import compute as c5

    p = c5.load("pages")
    X, y, test = np.asarray(p["X"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
    mu, sd = X[~test].mean(0), X[~test].std(0) + 1e-9
    Z = (X - mu) / sd
    return Z[~test], y[~test], Z[test], y[test], np.asarray(p["X2"])


# ---------------------------------------------------------------------------
def compute_gap():
    _, ytr, _, yte, X2 = pages()
    from videos.ai.ai5 import compute as c5

    p = c5.load("pages")
    test = np.asarray(p["test"], bool)
    A, B, _, _ = c5.standardize(X2[~test], X2[test])  # exactly as Part 5 did (the rates tie often; ties must break alike)
    dAA = ((A[:, None] - A[None]) ** 2).sum(-1)
    dBA = ((B[:, None] - A[None]) ** 2).sum(-1)
    oA, oB = np.argsort(dAA, 1, kind="stable"), np.argsort(dBA, 1, kind="stable")
    ks = np.arange(1, 152, 2)
    tr = [float(((ytr[oA[:, :k]].mean(1) > 0.5) == ytr).mean()) for k in ks]
    te = [float(((ytr[oB[:, :k]].mean(1) > 0.5) == yte).mean()) for k in ks]
    best = int(ks[int(np.argmax(te))])
    return dict(ks=ks, train_err=1 - np.array(tr), test_err=1 - np.array(te), best_k=best)


# ---------------------------------------------------------------------------
def truth(x):
    return np.sin(2.4 * x) + 0.3 * x


def compute_biasvar():
    g = rng(1992)  # Geman, Bienenstock & Doursat, 1992
    n, sigma, degs, runs = 16, 0.35, list(range(0, 16)), 200
    xg = np.linspace(-1.5, 1.5, 160)  # judged between the points, never beyond them
    fits = {d: [] for d in degs}
    xs_all = []
    for _ in range(runs):
        x = np.linspace(-1.6, 1.6, n) + g.uniform(-0.06, 0.06, n)
        yv = truth(x) + sigma * g.normal(size=n)
        xs_all.append((x, yv))
        for d in degs:
            V = np.vander(x / 1.6, d + 1)
            c = np.linalg.lstsq(V, yv, rcond=None)[0]
            fits[d].append(np.vander(xg / 1.6, d + 1) @ c)
    bias2, var = [], []
    for d in degs:
        F = np.array(fits[d])
        mean = F.mean(0)
        bias2.append(float(((mean - truth(xg)) ** 2).mean()))
        var.append(float(F.var(0).mean()))
    bias2, var = np.array(bias2), np.array(var)
    total = bias2 + var + sigma ** 2
    best = int(np.argmin(total))
    assert 3 <= best <= 9 and var[-1] > 100 * var[best] and bias2[0] > 10 * bias2[best]
    return dict(degs=degs, bias2=bias2, var=var, noise=sigma ** 2, total=total, best=best, xg=xg, truth=truth(xg),
                sample_x=xs_all[0][0], sample_y=xs_all[0][1], fits_1=np.array(fits[1][:20]),
                fits_best=np.array(fits[best][:20]), fits_top=np.array(fits[12][:20]), top=12, n=n,
                runs=runs)


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


# ---------------------------------------------------------------------------
def compute_rademacher():
    Ztr, ytr, _, _, _ = pages()
    g = rng(1960)
    n = len(ytr)
    ds = [1, 2, 3, 5, 8, 12, 20, 30, 45, 70]
    import torch

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


# ---------------------------------------------------------------------------
def compute_random():
    import torch

    Ztr, ytr, Zte, yte, _ = pages()
    torch.manual_seed(2016)  # Zhang et al. trained in 2016 (published 2017)
    g = rng(2017)
    Xtr, Xte = torch.tensor(Ztr, dtype=torch.float32), torch.tensor(Zte, dtype=torch.float32)
    out = {}
    for name, labels in (("true", ytr), ("shuffled", g.permutation(ytr))):
        torch.manual_seed(7)
        net = torch.nn.Sequential(torch.nn.Linear(Ztr.shape[1], 512), torch.nn.ReLU(), torch.nn.Linear(512, 512),
                                  torch.nn.ReLU(), torch.nn.Linear(512, 2))
        opt = torch.optim.Adam(net.parameters(), lr=1e-3)
        t = torch.tensor(labels, dtype=torch.long)
        curve = []
        for step in range(1, 1501):
            opt.zero_grad()
            loss = torch.nn.functional.cross_entropy(net(Xtr), t)
            loss.backward()
            opt.step()
            if step % 10 == 0 or step < 10:
                with torch.no_grad():
                    tr = float((net(Xtr).argmax(1) == t).float().mean())
                    te = float((net(Xte).argmax(1).numpy() == yte).mean())
                curve.append((step, tr, te, float(loss)))
        out[name] = np.array(curve)
    n_params = sum(p.numel() for p in net.parameters())
    assert out["shuffled"][-1, 1] == 1.0 and abs(out["shuffled"][-1, 2] - 0.5) < 0.1 and out["true"][-1, 2] > 0.95
    first = {k: int(v[np.argmax(v[:, 1] >= 1.0), 0]) for k, v in out.items()}
    return dict(true=out["true"], shuffled=out["shuffled"], n_params=int(n_params), n=len(ytr), first100=first)


# ---------------------------------------------------------------------------
def compute_double():
    Ztr, ytr, Zte, yte, _ = pages()
    g = rng(2019)  # Belkin, Hsu, Ma & Mandal, 2019
    n, d = Ztr.shape
    ps = np.unique(np.round(np.logspace(np.log10(10), np.log10(6000), 46)).astype(int))
    ps = np.unique(np.concatenate([ps, [n - 8, n, n + 8]]))
    ttr, tte = 2.0 * ytr - 1, 2.0 * yte - 1
    errs, tr_errs, norms = [], [], []
    reps = 5
    for p in ps:
        e, et, nm = [], [], []
        for r in range(reps):
            W = g.normal(size=(d, p)) / math.sqrt(d)
            Ftr, Fte = np.maximum(Ztr @ W, 0), np.maximum(Zte @ W, 0)
            beta = np.linalg.pinv(Ftr) @ ttr  # least squares, or the smallest solution that fits exactly
            e.append(float(((Fte @ beta - tte) ** 2).mean()))
            et.append(float(((Ftr @ beta - ttr) ** 2).mean()))
            nm.append(float(np.linalg.norm(beta)))
        errs.append(np.median(e))
        tr_errs.append(np.median(et))
        norms.append(np.median(nm))
    errs, tr_errs = np.array(errs), np.array(tr_errs)
    k_n = int(np.argmin(np.abs(ps - n)))
    assert errs[k_n] > 3 * errs[0] and errs[-1] < errs[k_n] / 3 and tr_errs[-1] < 1e-6
    return dict(ps=ps, test=errs, train=tr_errs, norms=np.array(norms), n=n, d=d, peak=float(errs[k_n]))


ITEMS = {
    "gap": compute_gap,
    "biasvar": compute_biasvar,
    "shatter": compute_shatter,
    "rademacher": compute_rademacher,
    "random": compute_random,
    "double": compute_double,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
