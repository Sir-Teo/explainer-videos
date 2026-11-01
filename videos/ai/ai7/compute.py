"""Precompute everything numerical in Part 7 of the AI series ("Statistical ML").

    python -m videos.ai.ai7.compute              # everything missing (needs Part 1's books and Part 6's pages)
    python -m videos.ai.ai7.compute --force hmm

Results are cached in ``.cache/ai7/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Every method is written
out here in numpy, and every number the narration quotes is computed here.

Items:
    pca      principal components of Part 6's 639 pages (70 word rates each, standardized): the variance each
             direction explains, the pages in the first three, and the words that load on the first two
    gmm      a mixture of two Gaussians fitted by EM to the pages' first two principal components, with no labels:
             every iteration's means, covariances, weights and log-likelihood; agreement with the true authors
    hmm      a two-state hidden Markov model fitted by Baum-Welch to 200,000 letters of the books: the emission
             probabilities at each iteration, the transition matrix, and the most likely states of a sentence
    gp       Gaussian-process regression on the rate of "her" across the pages of Great Expectations: the length
             scale chosen by marginal likelihood, prior and posterior samples, the mean and its band
    vi       variational inference on Part 5's two-bump density: the best single Gaussian under KL(q||p) and under
             KL(p||q), and the path of gradient steps on the ELBO
    kn       Kneser-Ney smoothing for character n-grams on Part 1's books, up to 7 characters of context: bits per character on the
             passage, the scoreboard's new row
"""

from __future__ import annotations

import math

import numpy as np

from .cache_contract import SchemaCache

CACHE = SchemaCache("ai7")


def load(name):
    return CACHE.load(name)


def cache_current(name):
    return CACHE.current(name)


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def ai1():
    from videos.ai.ai1 import compute as c1

    return c1


def pages():
    p = CACHE.read_pages()
    return np.asarray(p["X"]), np.asarray(p["y"]), np.asarray(p["book"]), p["vocab"]


# ---------------------------------------------------------------------------
def compute_pca():
    X, y, book, vocab = pages()
    Z = (X - X.mean(0)) / X.std(0)
    C = Z.T @ Z / len(Z)
    vals, vecs = np.linalg.eigh(C)
    o = np.argsort(-vals)
    vals, vecs = vals[o], vecs[:, o]
    vecs *= np.sign(vecs[np.argmax(np.abs(vecs), 0), np.arange(vecs.shape[1])])  # a fixed sign convention
    proj = Z @ vecs[:, :3]
    if proj[y == 1, 0].mean() < proj[y == 0, 0].mean():  # Dickens to the right
        vecs[:, 0] *= -1
        proj[:, 0] *= -1
    share = vals / vals.sum()
    top = {k: [[vocab[i], float(vecs[i, k])] for i in np.argsort(-np.abs(vecs[:, k]))[:8]] for k in (0, 1)}
    # how well PC1 alone splits the authors (no labels were used to find it)
    thr = 0.5 * (proj[y == 0, 0].mean() + proj[y == 1, 0].mean())
    split = float(((proj[:, 0] > thr) == y).mean())
    assert np.all(np.diff(share) <= 1e-12)  # eigenspectrum order, independent of label agreement
    return dict(share=share, proj=proj, y=y, top=top, split=split, n=len(y), d=X.shape[1])


# ---------------------------------------------------------------------------
def gauss_logpdf(X, m, S):
    d = X - m
    inv = np.linalg.inv(S)
    return -0.5 * np.einsum("ni,ij,nj->n", d, inv, d) - 0.5 * math.log(np.linalg.det(2 * math.pi * S))


GMM_MIN_VARIANCE = 1e-6


def covariance_mle(scatter):
    """Exact covariance M step subject to Sigma >= GMM_MIN_VARIANCE * I.

    Flooring eigenvalues solves this constrained problem; adding a ridge to
    every eigenvalue would change the optimum and can decrease likelihood.
    """
    values, vectors = np.linalg.eigh(scatter)
    return (vectors * np.maximum(values, GMM_MIN_VARIANCE)) @ vectors.T


def compute_gmm():
    P = np.asarray(load("pca")["proj"])[:, :2]
    _, y, _, _ = pages()
    g = rng(1977)  # Dempster, Laird & Rubin, 1977
    means = np.array([[-0.5, 2.5], [0.5, 2.0]])  # a deliberately poor start
    covs = np.array([np.eye(2) * 0.8, np.eye(2) * 0.8])
    w = np.array([0.5, 0.5])
    hist = []
    for it in range(40):
        lp = np.stack([np.log(w[k]) + gauss_logpdf(P, means[k], covs[k]) for k in range(2)], 1)
        mx = lp.max(1, keepdims=True)
        ll = float((mx[:, 0] + np.log(np.exp(lp - mx).sum(1))).mean())
        r = np.exp(lp - mx)
        r /= r.sum(1, keepdims=True)  # E step: responsibilities
        hist.append(dict(means=means.copy(), covs=covs.copy(), w=w.copy(), ll=ll, r=r[:, 1].copy()))
        nk = r.sum(0)  # M step
        w = nk / len(P)
        means = (r.T @ P) / nk[:, None]
        covs = np.array([covariance_mle(((r[:, k:k + 1] * (P - means[k])).T @ (P - means[k])) / nk[k])
                         for k in range(2)])
    lls = [h["ll"] for h in hist]
    assert all(b >= a - 1e-9 for a, b in zip(lls, lls[1:]))  # EM never goes downhill
    lab = hist[-1]["r"] > 0.5
    agree = float(max((lab == y).mean(), (lab != y).mean()))
    del g
    return dict(P=P, y=y, means=np.array([h["means"] for h in hist]), covs=np.array([h["covs"] for h in hist]),
                w=np.array([h["w"] for h in hist]), ll=np.array(lls), r=np.array([h["r"] for h in hist]),
                agree=agree, covariance_floor=GMM_MIN_VARIANCE)


# ---------------------------------------------------------------------------
HMM_LETTERS = 200_000


def hmm_log_likelihood(obs, A, B, pi):
    """Scaled forward likelihood, including the final fitted replay state."""
    if len(obs) == 0:
        return 0.0
    alpha = pi * B[:, obs[0]]
    scale = float(alpha.sum())
    if scale == 0:
        return -math.inf
    value = math.log(scale)
    alpha /= scale
    for symbol in obs[1:]:
        alpha = (alpha @ A) * B[:, symbol]
        scale = float(alpha.sum())
        if scale == 0:
            return -math.inf
        value += math.log(scale)
        alpha /= scale
    return value


def baum_welch(obs, K, S, iters, seed):
    g = rng(seed)
    A = np.full((S, S), 1 / S) + g.uniform(-0.05, 0.05, (S, S))
    A /= A.sum(1, keepdims=True)
    B = g.uniform(0.5, 1.5, (S, K))
    B /= B.sum(1, keepdims=True)
    pi = np.full(S, 1 / S)
    T = len(obs)
    Bs, lls = [B.copy()], []
    for _ in range(iters):
        # forward-backward with scaling
        al = np.empty((T, S))
        c = np.empty(T)
        al[0] = pi * B[:, obs[0]]
        c[0] = al[0].sum()
        al[0] /= c[0]
        for t in range(1, T):
            al[t] = (al[t - 1] @ A) * B[:, obs[t]]
            c[t] = al[t].sum()
            al[t] /= c[t]
        be = np.empty((T, S))
        be[-1] = 1.0
        for t in range(T - 2, -1, -1):
            be[t] = (A @ (B[:, obs[t + 1]] * be[t + 1])) / c[t + 1]
        lls.append(float(np.log(c).sum() / T))
        gam = al * be
        gam /= gam.sum(1, keepdims=True)
        xi = (al[:-1, :, None] * A[None] * (B[:, obs[1:]].T * be[1:])[:, None, :]) / c[1:, None, None]
        A = xi.sum(0) / xi.sum((0, 2))[:, None]
        B = np.stack([np.bincount(obs, weights=gam[:, s], minlength=K) for s in range(S)])
        B /= B.sum(1, keepdims=True)
        pi = gam[0]
        Bs.append(B.copy())
    # Bs includes the initial model and every M step; score the final one too.
    lls.append(hmm_log_likelihood(obs, A, B, pi) / T)
    return A, B, pi, np.array(Bs), np.array(lls)


def viterbi(obs, A, B, pi):
    T, S = len(obs), len(pi)
    lA, lB = np.log(A), np.log(B + 1e-300)
    d = np.log(pi + 1e-300) + lB[:, obs[0]]
    back = np.zeros((T, S), int)
    for t in range(1, T):
        m = d[:, None] + lA
        back[t] = np.argmax(m, 0)
        d = m.max(0) + lB[:, obs[t]]
    path = [int(np.argmax(d))]
    for t in range(T - 1, 0, -1):
        path.append(int(back[t][path[-1]]))
    return path[::-1]


def compute_hmm():
    c1 = ai1()
    t = CACHE.read_text("train27")[:HMM_LETTERS]
    alpha = c1.ALPHA27
    obs = np.array([alpha.index(ch) for ch in t])
    A, B, pi, Bs, lls = baum_welch(obs, 27, 2, 60, seed=1980)  # Cave & Neuwirth, 1980
    # which state is the vowel state?
    vow = [alpha.index(v) for v in "aeiou"]
    sv = int(np.argmax(B[:, vow].sum(1)))
    if sv == 1:  # put the vowel state first
        A, B, pi, Bs = A[::-1, ::-1], B[::-1], pi[::-1], Bs[:, ::-1]
    post = B / B.sum(0, keepdims=True)  # which state emits each letter more (equal state weights)
    vowel_side = [alpha[i] for i in range(27) if B[0, i] > B[1, i]]
    sent = c1.to27("There is no reverse on a motorcycle")
    states = viterbi(np.array([alpha.index(ch) for ch in sent]), A, B, np.full(2, 0.5))  # no memory of the books' start
    assert all(b >= a - 1e-9 for a, b in zip(lls, lls[1:]))
    return dict(A=A, B=B, pi=pi, Bs=Bs, lls=lls / math.log(2), vowel_side=vowel_side, sentence=sent, states=states,
                n=len(obs), post=post)


# ---------------------------------------------------------------------------
def compute_gp():
    X, y, book, vocab = pages()
    j = vocab.index("her")
    yv = X[book == 1400, j]  # Great Expectations, page by page
    x = np.arange(len(yv), dtype=float)
    mu0 = float(yv.mean())
    yc = yv - mu0

    def kern(a, b, ell, s2):
        return s2 * np.exp(-0.5 * (a[:, None] - b[None]) ** 2 / ell ** 2)

    def mlik(ell, s2, n2):
        K = kern(x, x, ell, s2) + n2 * np.eye(len(x))
        L = np.linalg.cholesky(K)
        al = np.linalg.solve(L.T, np.linalg.solve(L, yc))
        return float(-0.5 * yc @ al - np.log(np.diag(L)).sum() - 0.5 * len(x) * math.log(2 * math.pi))

    v = float(yc.var())
    best = max(((mlik(ell, f * m * v, (1 - f) * m * v), ell, f * m * v, (1 - f) * m * v)
                for ell in (1.5, 2, 3, 4, 6, 8, 12, 16) for f in np.linspace(0.05, 0.95, 19) for m in (0.7, 1.0, 1.4)),
               key=lambda t_: t_[0])
    _, ell, s2, n2 = best
    xs = np.linspace(0, len(x) - 1, 300)
    K = kern(x, x, ell, s2) + n2 * np.eye(len(x))
    Ks = kern(xs, x, ell, s2)
    mean = Ks @ np.linalg.solve(K, yc)
    cov = kern(xs, xs, ell, s2) - Ks @ np.linalg.solve(K, Ks.T)
    sd = np.sqrt(np.maximum(np.diag(cov), 0))
    g = rng(1960)
    Lp = np.linalg.cholesky(kern(xs, xs, ell, s2) + 1e-6 * np.eye(len(xs)))
    Lq = np.linalg.cholesky(cov + 1e-6 * np.eye(len(xs)))
    prior = (Lp @ g.normal(size=(len(xs), 5))).T + mu0
    postS = (Lq @ g.normal(size=(len(xs), 5))).T + mean + mu0
    # the same, conditioned on only the first 20 pages: the band opens up beyond them
    m20 = 20
    K20 = kern(x[:m20], x[:m20], ell, s2) + n2 * np.eye(m20)
    Ks20 = kern(xs, x[:m20], ell, s2)
    mean20 = Ks20 @ np.linalg.solve(K20, yc[:m20])
    sd20 = np.sqrt(np.maximum(np.diag(kern(xs, xs, ell, s2) - Ks20 @ np.linalg.solve(K20, Ks20.T)), 0))
    return dict(x=x, y=yv, xs=xs, mean=mean + mu0, sd=sd, ell=ell, s2=s2, noise=n2, prior=prior, post=postS,
                mean20=mean20 + mu0, sd20=sd20, m20=m20, mu0=mu0, n_pages=len(x))


# ---------------------------------------------------------------------------
def compute_vi():
    from videos.ai.ai5.compute import density2

    xs, ys = np.linspace(-4, 4, 161), np.linspace(-3, 3, 121)
    X, Y = np.meshgrid(xs, ys)
    G = np.stack([X.ravel(), Y.ravel()], 1)
    p = density2(X, Y).ravel()
    p /= p.sum()
    logp = np.log(p + 1e-300)

    def q_of(theta):
        m, ls, r = theta[:2], theta[2:4], math.tanh(theta[4])
        s = np.exp(ls)
        S = np.array([[s[0] ** 2, r * s[0] * s[1]], [r * s[0] * s[1], s[1] ** 2]])
        lq = gauss_logpdf(G, m, S)
        q = np.exp(lq - lq.max())
        q /= q.sum()
        return q, np.log(q + 1e-300)

    def kl_qp(theta):
        q, lq = q_of(theta)
        return float((q * (lq - logp)).sum())

    def kl_pq(theta):
        q, lq = q_of(theta)
        return float((p * (logp - lq)).sum())

    from scipy.optimize import minimize

    path = []
    th0 = np.array([-0.2, 1.5, -0.5, -0.5, 0.0])  # a poor start, above the two bumps
    reverse = minimize(kl_qp, th0, method="Nelder-Mead", callback=lambda th: path.append(th.copy()),
                       options=dict(maxiter=600, xatol=1e-4, fatol=1e-7))
    t_qp = reverse.x
    path.append(t_qp.copy())
    # Moment matching initializes an untruncated Gaussian. Here q is normalized
    # on the finite plotting grid, so optimize that actual objective too.
    mean_p = p @ G
    cov_p = ((G - mean_p) * p[:, None]).T @ (G - mean_p)
    sd_p = np.sqrt(np.diag(cov_p))
    initial_pq = np.array([*mean_p, *np.log(sd_p), math.atanh(cov_p[0, 1] / (sd_p[0] * sd_p[1]))])
    forward = minimize(kl_pq, initial_pq, method="BFGS", options=dict(gtol=1e-7, maxiter=600))
    t_pq = forward.x
    pick = np.linspace(0, len(path) - 1, 40).astype(int)
    return dict(path=np.array(path)[pick], t_qp=t_qp, t_pq=t_pq, mean_p=mean_p, cov_p=cov_p,
                kl_qp=[kl_qp(path[k]) for k in pick], kl_final=kl_qp(t_qp), kl_pq_final=kl_pq(t_pq),
                initial_forward_kl=kl_pq(initial_pq),
                objective_scope="Both distributions discretized and normalized on the displayed finite grid",
                reverse_optimizer=dict(success=bool(reverse.success), message=str(reverse.message)),
                forward_optimizer=dict(success=bool(forward.success), message=str(forward.message)))


# ---------------------------------------------------------------------------
def ngram_tables(a, K, M):
    """The distinct n-grams of a (lengths 1..M+1) and their counts."""
    n = len(a)
    tables = []
    for m in range(M + 1):
        L = m + 1  # the n-gram (context + next symbol)
        key = np.zeros(n - L + 1, np.int64)
        for j in range(L):
            key = key * K + a[j:n - L + 1 + j]
        types, cnt = np.unique(key, return_counts=True)
        tables.append(dict(types=types, cnt=cnt))
    return tables


def kn_model(tables, K, M):
    """Interpolated Kneser-Ney for symbol sequences, context lengths 0..M: the tables a scorer needs.  Below the top
    order, counts are continuation counts: N1+(. h c), the number of distinct symbols seen before (h c)."""
    model = []
    for m in range(M + 1):
        L = m + 1
        if m == M:
            keys, c = tables[m]["types"], tables[m]["cnt"].astype(float)
        else:
            longer = tables[m + 1]["types"] % (K ** L)  # drop the first symbol
            keys, c = np.unique(longer, return_counts=True)
            c = c.astype(float)
        n1, n2 = float((c == 1).sum()), float((c == 2).sum())
        D = n1 / (n1 + 2 * n2) if n1 + n2 > 0 else 0.5
        ctx = keys // K
        cu, inv = np.unique(ctx, return_inverse=True)
        tot = np.bincount(inv, weights=c)
        ntypes = np.bincount(inv)
        model.append(dict(keys=keys, c=c, D=D, ctx=cu, tot=tot, ntypes=ntypes))
    return model


def kn_bits(model, a, K, M, *, start=None):
    """Bits per scored symbol; default start M preserves the natural-order cohort."""
    return float(-np.log2(kn_probs(model, a, K, M, start=start)).mean())


def kn_probs(model, a, K, M, *, start=None):
    """Probability at each target from start (default M); no empty/padded cohort."""
    n = len(a)
    start = M if start is None else start
    if (not isinstance(start, (int, np.integer)) or isinstance(start, (bool, np.bool_))
            or not M <= start < n):
        raise ValueError("KN evaluation requires an integer start >= order and a nonempty suffix")
    idx = np.arange(start, n)
    p = np.full(len(idx), 1.0 / K)
    for m in range(M + 1):
        t = model[m]
        key = np.zeros(len(idx), np.int64)
        for j in range(m, -1, -1):
            key = key * K + a[idx - j]
        ctx = key // K
        i = np.minimum(np.searchsorted(t["keys"], key), len(t["keys"]) - 1)
        c = np.where(t["keys"][i] == key, t["c"][i], 0.0)
        k = np.minimum(np.searchsorted(t["ctx"], ctx), len(t["ctx"]) - 1)
        seen = t["ctx"][k] == ctx
        tot = np.where(seen, t["tot"][k], 0.0)
        nt = np.where(seen, t["ntypes"][k], 0.0)
        safe = np.maximum(tot, 1.0)
        new = np.maximum(c - t["D"], 0) / safe + t["D"] * nt / safe * p
        p = np.where(seen, new, p)
    return p


def compute_kn():
    train, valid, passage = CACHE.read_text("train"), CACHE.read_text("valid"), CACHE.read_text("passage")
    chars = sorted(set(train) | set(valid) | set(passage))
    idx = {ch: i for i, ch in enumerate(chars)}
    K = len(chars)
    enc = lambda t: np.array([idx[ch] for ch in t], np.int64)  # noqa: E731
    a, v, ps = enc(train), enc(valid), enc(passage)
    MAXM = max(m for m in range(1, 10) if K ** (m + 1) < 2 ** 62)  # n-gram keys must fit in 64 bits
    if min(len(a), len(v), len(ps)) <= MAXM:
        raise ValueError("KN comparison requires training n-grams and nonempty validation/passage suffixes at the maximum order")
    rows = []
    tables = ngram_tables(a, K, MAXM)
    for M in range(0, MAXM + 1):
        model = kn_model(tables, K, M)
        rows.append(dict(order=M, start=MAXM, valid_count=len(v) - MAXM, test_count=len(ps) - MAXM,
                         valid=kn_bits(model, v, K, M, start=MAXM),
                         test=kn_bits(model, ps, K, M, start=MAXM)))
        print(f"    KN order {M}: valid {rows[-1]['valid']:.3f}  passage {rows[-1]['test']:.3f}")
    best = int(np.argmin([r["valid"] for r in rows]))
    selected = kn_model(tables, K, best)
    same_order = dict(order=best, start=best, valid_count=len(v) - best, test_count=len(ps) - best,
                      valid=kn_bits(selected, v, K, best), test=kn_bits(selected, ps, K, best))
    raw = CACHE.read_part1("raw")
    return dict(K=K, rows=rows, best=best, best_bits=same_order["test"],
                comparison_best_bits=rows[best]["test"], comparison_start=MAXM,
                valid_count=len(v) - MAXM, test_count=len(ps) - MAXM, selected_same_order=same_order,
                part1_best=raw["best_bits"],
                part1_rows=[r["test"] for r in raw["rows"]])


# ===========================================================================
# The expansion: every item below is new; the six above are read by other parts and stay as they are.
# ===========================================================================
def glogpdf(X, m, S):
    """Gaussian log density, through slogdet (safe in 70 dimensions)."""
    d = X - m
    sign, logdet = np.linalg.slogdet(S)
    assert sign > 0
    sol = np.linalg.solve(S, d.T).T
    return -0.5 * (d * sol).sum(1) - 0.5 * (logdet + S.shape[0] * math.log(2 * math.pi))


def compute_pca2():
    X, y, book, vocab = pages()
    test = np.asarray(CACHE.read_pages()["test"], bool)
    Z = (X - X.mean(0)) / X.std(0)
    n, d = Z.shape
    vals, vecs = np.linalg.eigh(Z.T @ Z / n)
    o = np.argsort(-vals)
    vals, vecs = vals[o], vecs[:, o]
    # two ways of saying the same thing: the variance a k-dimensional subspace keeps, the squared error it leaves
    kept = np.array([((Z @ vecs[:, :k]) ** 2).sum(1).mean() for k in range(d + 1)])
    err = np.array([((Z - Z @ vecs[:, :k] @ vecs[:, :k].T) ** 2).sum(1).mean() for k in range(d + 1)])
    tail = np.array([vals[k:].sum() for k in range(d + 1)])
    assert np.allclose(kept + err, d) and np.allclose(err, tail)
    sv = np.linalg.svd(Z, compute_uv=False)  # Part 3's SVD of the data matrix itself
    assert np.allclose(sv ** 2 / n, vals)
    # the picture in two of the 70 rates: along a line at angle theta, kept + lost = the total, for every theta
    Z2 = Z[:, [vocab.index("the"), vocab.index("not")]]
    th = np.linspace(0, np.pi, 181)
    U = np.stack([np.cos(th), np.sin(th)], 1)
    along = ((Z2 @ U.T) ** 2).mean(0)
    lost = (Z2 ** 2).sum(1).mean() - along
    # probabilistic PCA (Tipping & Bishop, 1999): fitted on Part 6's training pages, scored on its held-out pages
    Xtr, Xte = X[~test], X[test]
    mu, sd = Xtr.mean(0), Xtr.std(0)
    Ztr, Zte = (Xtr - mu) / sd, (Xte - mu) / sd
    lv, lV = np.linalg.eigh(Ztr.T @ Ztr / len(Ztr))
    o = np.argsort(-lv)
    lv, lV = lv[o], lV[:, o]
    ll_tr, ll_te, sig2 = [], [], []
    for k in range(d):
        s2 = float(lv[k:].mean())  # the noise: the average variance of the directions left out
        W = lV[:, :k] * np.sqrt(np.maximum(lv[:k] - s2, 0))
        Cm = W @ W.T + s2 * np.eye(d)
        ll_tr.append(float(glogpdf(Ztr, 0, Cm).mean()))
        ll_te.append(float(glogpdf(Zte, 0, Cm).mean()))
        sig2.append(s2)
    full_te = float(glogpdf(Zte, 0, Ztr.T @ Ztr / len(Ztr) + 1e-9 * np.eye(d)).mean())
    best_k = int(np.argmax(ll_te))
    assert all(b >= a - 1e-9 for a, b in zip(ll_tr, ll_tr[1:]))  # more directions never fit the training pages worse
    return dict(vals=vals, kept=kept, err=err, sv=sv, n=n, d=d, theta=th, along=along, lost=lost,
                total2=float((Z2 ** 2).sum(1).mean()), th_best=float(th[np.argmax(along)]),
                Z2=Z2, ll_tr=np.array(ll_tr), ll_te=np.array(ll_te), sig2=np.array(sig2), best_k=best_k,
                full_te=full_te, n_train=int((~test).sum()), n_test=int(test.sum()),
                share5=float(vals[:5].sum() / vals.sum()), share_best=float(vals[:best_k].sum() / vals.sum()),
                training_share_best=float(lv[:best_k].sum() / lv.sum()))


# ---------------------------------------------------------------------------
def bijective_correlations(correlation):
    """Best total absolute correlation, with each of two sources used once."""
    matrix = np.abs(np.asarray(correlation, float))
    if matrix.shape != (2, 2) or not np.isfinite(matrix).all():
        raise ValueError("A finite two-output, two-source correlation matrix is required")
    assignment = (0, 1) if np.trace(matrix) >= np.trace(matrix[:, ::-1]) else (1, 0)
    return matrix[np.arange(2), assignment]


def compute_ica():
    """Two voices, two microphones: a tone and a sawtooth, mixed; whitening, then the rotation that makes the outputs
    least Gaussian, found by FastICA's fixed point on the kurtosis."""
    T = 4000
    t = np.linspace(0, 8, T)
    S = np.stack([np.sin(2 * np.pi * 0.9 * t + 0.3), 2 * ((0.55 * t + 0.2) % 1) - 1])
    S = (S - S.mean(1, keepdims=True)) / S.std(1, keepdims=True)
    A = np.array([[0.9, 0.55], [0.4, 1.0]])  # how loud each voice is at each microphone
    X = A @ S
    Xc = X - X.mean(1, keepdims=True)
    ev, E = np.linalg.eigh(Xc @ Xc.T / T)
    Xw = np.diag(ev ** -0.5) @ E.T @ Xc  # whitened: uncorrelated, unit variance (this is all PCA can do)
    th = np.linspace(0, np.pi, 361)
    kurt = np.array([((np.cos(a) * Xw[0] + np.sin(a) * Xw[1]) ** 4).mean() - 3 for a in th])
    g = rng(1999)  # Hyvarinen, 1999
    a0 = float(g.uniform(0, np.pi))
    w = np.array([math.cos(a0), math.sin(a0)])
    path = [w.copy()]
    for _ in range(40):
        u = w @ Xw
        w1 = (Xw * u ** 3).mean(1) - 3 * w  # the fixed point of the kurtosis contrast
        w1 /= np.linalg.norm(w1)
        if w1 @ w < 0:
            w1 = -w1
        path.append(w1.copy())
        done = 1 - abs(w1 @ w) < 1e-12
        w = w1
        if done:
            break
    w2 = np.array([-w[1], w[0]])
    Y = np.stack([w @ Xw, w2 @ Xw])
    R = np.corrcoef(np.vstack([Y, S]))[:2, 2:]
    perm = [int(np.argmax(np.abs(R[0]))), 1 - int(np.argmax(np.abs(R[0])))]
    Y = np.stack([Y[perm.index(0)], Y[perm.index(1)]])  # recovered source k matches true source k
    Y *= np.sign(np.sum(Y * S, 1))[:, None]
    r_ica = np.abs(np.corrcoef(np.vstack([Y, S]))[:2, 2:]).diagonal()
    r_pca = bijective_correlations(np.corrcoef(np.vstack([Xw, S]))[:2, 2:])
    r_mic = bijective_correlations(np.corrcoef(np.vstack([X, S]))[:2, 2:])
    ang = np.array([math.atan2(p[1], p[0]) % np.pi for p in path])
    sub = np.arange(0, T, 5)
    return dict(t=t[sub], S=S[:, sub], X=X[:, sub], Xw=Xw[:, sub], Y=Y[:, sub], A=A, theta=th, kurt=kurt, ang=ang,
                iters=len(path) - 1, r_ica=r_ica, r_pca=r_pca, r_mic=r_mic, kurt_src=(S ** 4).mean(1) - 3,
                kurt_mix=(Xw ** 4).mean(1) - 3)


# ---------------------------------------------------------------------------
def gmm_params(g, k):
    return np.asarray(g["means"])[k], np.asarray(g["covs"])[k], np.asarray(g["w"])[k]


def gmm_logjoint(P, m, S, w):
    return np.stack([math.log(w[z]) + gauss_logpdf(P, m[z], S[z]) for z in range(len(w))], 1)


def compute_embound():
    """The EM bound, drawn for real: along the line from round k's parameters to round k+1's, the log-likelihood and
    the lower bound that round k's E step built.  They touch at round k; the bound peaks at round k+1."""
    g = load("gmm")
    P = np.asarray(g["P"])
    ts = np.linspace(-0.5, 1.6, 85)
    i0, i1 = int(np.argmin(np.abs(ts))), int(np.argmin(np.abs(ts - 1)))
    out = []
    for k in (0, 1, 2, 4):
        m0, S0, w0 = gmm_params(g, k)
        m1, S1, w1 = gmm_params(g, k + 1)
        lj = gmm_logjoint(P, m0, S0, w0)
        mx = lj.max(1, keepdims=True)
        q = np.exp(lj - mx)
        q /= q.sum(1, keepdims=True)  # round k's E step
        ll, bd = [], []
        for t in ts:
            m, S, w = m0 + t * (m1 - m0), S0 + t * (S1 - S0), w0 + t * (w1 - w0)
            if ((w <= 0).any()
                    or any(np.linalg.eigvalsh(S[z]).min() < GMM_MIN_VARIANCE * (1 - 1e-9) for z in range(2))):
                ll.append(np.nan)
                bd.append(np.nan)
                continue
            lp = gmm_logjoint(P, m, S, w)
            mm = lp.max(1, keepdims=True)
            ll.append(float((mm[:, 0] + np.log(np.exp(lp - mm).sum(1))).mean()))
            bd.append(float((q * (lp - np.log(q + 1e-300))).sum(1).mean()))
        ll, bd = np.array(ll), np.array(bd)
        ok = np.isfinite(ll)
        assert abs(ll[i0] - bd[i0]) < 1e-9 and (bd[ok] <= ll[ok] + 1e-9).all()  # Jensen: below, touching at round k
        assert abs(int(np.nanargmax(bd)) - i1) <= 1  # the M step: the bound's top is round k+1
        assert abs(ll[i0] - float(np.asarray(g["ll"])[k])) < 1e-9
        out.append(dict(k=k, ll=ll, bound=bd))
    return dict(ts=ts, i0=i0, i1=i1, rounds=[o["k"] for o in out], ll=np.array([o["ll"] for o in out]),
                bound=np.array([o["bound"] for o in out]))


def compute_kmeans():
    g = load("gmm")
    P, y = np.asarray(g["P"]), np.asarray(g["y"])
    C = np.array([[-0.5, 2.5], [0.5, 2.0]])  # the same poor start as EM
    cs, zs, J = [], [], []
    for _ in range(50):
        d2 = ((P[:, None] - C[None]) ** 2).sum(2)
        z = np.argmin(d2, 1)
        cs.append(C.copy())
        zs.append(z.copy())
        J.append(float(d2[np.arange(len(P)), z].mean()))
        C1 = np.array([P[z == k].mean(0) for k in range(2)])
        if np.allclose(C1, C):
            break
        C = C1
    assert all(b <= a + 1e-12 for a, b in zip(J, J[1:]))  # Lloyd's steps never raise the objective
    z = zs[-1]
    agree = float(max((z == y).mean(), (z != y).mean()))
    em = np.asarray(g["r"])[-1] > 0.5
    same = float(max((z == em).mean(), (z != em).mean()))
    # hard EM: equal bells of shared width sigma at the final centres; as sigma shrinks, every responsibility is 0 or 1
    sig = np.array([3.0, 2.0, 1.4, 1.0, 0.7, 0.5, 0.35, 0.25, 0.15, 0.1])
    d2 = ((P[:, None] - C[None]) ** 2).sum(2)
    hard = []
    for s in sig:
        lp = -d2 / (2 * s * s)
        r = np.exp(lp - lp.max(1, keepdims=True))
        r /= r.sum(1, keepdims=True)
        hard.append(float((r.max(1) > 0.99).mean()))
    return dict(centres=np.array(cs), z=np.array(zs), J=np.array(J), iters=len(J), agree=agree, same_as_em=same,
                agree_em=float(g["agree"]), sigma=sig, hard=np.array(hard))


# ---------------------------------------------------------------------------
# Topic models: latent Dirichlet allocation by variational EM (Blei, Ng & Jordan, 2003)
LDA_K, LDA_SEG, LDA_V, LDA_ITERS, LDA_INNER, LDA_ALPHA, LDA_ETA = 12, 2000, 3000, 40, 4, 0.1, 0.01
STOP = set("""a about above after again against all am an and any are as at be because been before being below between
both but by can could did do does doing down during each few for from further had has have having he her here hers
herself him himself his how i if in into is it its itself just me more most my myself no nor not now of off on once
only or other our ours ourselves out over own same she should so some such than that the their theirs them themselves
then there these they this those through to too under until up very was we were what when where which while who whom
why will with would you your yours yourself yourselves said say says one upon shall may might must every much many like
well yet also even though thus ever never quite rather again come came go went see seen saw know knew made make little
nothing something thing things way time could would should""".split())


def lda_corpus():
    import collections
    import re
    import unicodedata

    c1 = ai1()
    segs, sbook = [], []
    cap, low = collections.Counter(), collections.Counter()
    for n in c1.BOOKS:
        t = c1.strip_gutenberg(CACHE.read_book(n))
        t = unicodedata.normalize("NFKD", t.translate(c1.QUOTES).replace("_", "")).encode("ascii", "ignore").decode()
        toks = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", t)
        for w in toks:
            (cap if w[0].isupper() else low)[w.lower()] += 1
        lw = [w.lower() for w in toks]
        for i in range(0, len(lw) - LDA_SEG + 1, LDA_SEG):
            segs.append(lw[i:i + LDA_SEG])
            sbook.append(n)
    names = {w for w in cap if cap[w] > low[w]}  # mostly capitalized: names and places
    keep = lambda w: len(w) > 2 and "'" not in w and w not in STOP and w not in names  # noqa: E731
    df, tot = collections.Counter(), collections.Counter()
    for s in segs:
        c = collections.Counter(w for w in s if keep(w))
        tot.update(c)
        df.update(c.keys())
    vocab = [w for w, _ in tot.most_common() if df[w] <= 0.25 * len(segs)][:LDA_V]
    vid = {w: i for i, w in enumerate(vocab)}
    di, wi, cn = [], [], []
    for d, s in enumerate(segs):
        c = collections.Counter(vid[w] for w in s if w in vid)
        for w, k in c.items():
            di.append(d)
            wi.append(w)
            cn.append(k)
    return (np.array(di), np.array(wi), np.array(cn, float), vocab, np.array(sbook), segs, vid,
            len(names))


def compute_lda():
    from scipy.special import digamma, gammaln

    di, wi, cn, vocab, sbook, segs, vid, n_names = lda_corpus()
    D, V, K = len(sbook), len(vocab), LDA_K
    g = rng(2003)  # Blei, Ng & Jordan, 2003
    beta = np.full((K, V), LDA_ETA)
    for k in range(K):  # each topic starts as the words of a few random sections
        for d in g.choice(D, size=3, replace=False):
            sel = di == d
            np.add.at(beta[k], wi[sel], cn[sel])
    beta /= beta.sum(1, keepdims=True)
    nd = np.bincount(di, weights=cn, minlength=D)
    gamma = LDA_ALPHA + nd[:, None] / K + g.uniform(0, 1, (D, K))
    N = cn.sum()
    bounds, snaps, snap_at = [], {}, (0, 1, 2, 3, 5, 8, 13, 20, 30, LDA_ITERS)

    def top(b, m=8):
        return [[vocab[i] for i in np.argsort(-b[k])[:m]] for k in range(K)]

    def bound():
        Elog = digamma(gamma) - digamma(gamma.sum(1))[:, None]
        value = (D * (gammaln(K * LDA_ALPHA) - K * gammaln(LDA_ALPHA)) + (LDA_ALPHA - 1) * Elog.sum()
                 + (cn[:, None] * phi * (Elog[di] + np.log(beta.T[wi]) - np.log(phi + 1e-300))).sum()
                 - (gammaln(gamma.sum(1)) - gammaln(gamma).sum(1)
                    + ((gamma - 1) * Elog).sum(1)).sum())
        return float(value / N)

    initial_logphi = (digamma(gamma) - digamma(gamma.sum(1))[:, None])[di] + np.log(beta.T[wi])
    phi = np.exp(initial_logphi - initial_logphi.max(1, keepdims=True))
    phi /= phi.sum(1, keepdims=True)
    snaps["0"] = top(beta)
    bounds.append(bound())
    for it in range(1, LDA_ITERS + 1):
        for _ in range(LDA_INNER):  # E step: coordinate ascent on each section's q(theta) and q(z)
            Elog = digamma(gamma) - digamma(gamma.sum(1))[:, None]
            lphi = Elog[di] + np.log(beta.T[wi])
            lphi -= lphi.max(1, keepdims=True)
            phi = np.exp(lphi)
            phi /= phi.sum(1, keepdims=True)
            gamma = LDA_ALPHA + np.stack([np.bincount(di, weights=cn * phi[:, k], minlength=D) for k in range(K)], 1)
        # M step: each topic's word probabilities from the words it was given
        beta = np.stack([np.bincount(wi, weights=cn * phi[:, k], minlength=V) for k in range(K)]) + LDA_ETA
        beta /= beta.sum(1, keepdims=True)
        # The replay's round-it topics and bound must use this same post-M beta.
        bounds.append(bound())
        if it in snap_at:
            snaps[str(it)] = top(beta)
        print(f"    LDA round {it}: bound {bounds[-1]:.4f} nats per word", flush=True)
    theta = gamma / gamma.sum(1, keepdims=True)
    size = (theta * nd[:, None]).sum(0)
    order = np.argsort(-size)  # topics by how many words they hold
    beta, theta, size = beta[order], theta[:, order], size[order]
    snaps = {k: [v[j] for j in order] for k, v in snaps.items()}
    c1 = ai1()
    books = list(c1.BOOKS)
    share = np.array([[(theta[sbook == b, k] * nd[sbook == b]).sum() for b in books] for k in range(K)])
    share /= share.sum(1, keepdims=True)
    main = [books[int(np.argmax(share[k]))] for k in range(K)]
    # one section that mixes two topics most evenly, its mixture, and its words coloured by their likeliest topic
    srt = np.sort(theta, 1)
    ex = int(np.argmax(np.minimum(srt[:, -1], srt[:, -2]) * (srt[:, -1] + srt[:, -2] > 0.85)))
    Elog = digamma(gamma[:, order]) - digamma(gamma.sum(1))[:, None]
    words = segs[ex][:400]
    col = [int(np.argmax(Elog[ex] + np.log(beta[:, vid[w]]))) if w in vid else -1 for w in words]
    mono = all(b >= a - 1e-6 for a, b in zip(bounds, bounds[1:]))
    return dict(K=K, V=V, D=D, seg=LDA_SEG, alpha=LDA_ALPHA, n_names=n_names, words_total=int(N), bounds=bounds,
                bound_rounds=list(range(LDA_ITERS + 1)),
                monotone=mono, snaps=snaps, top=[[vocab[i] for i in np.argsort(-beta[k])[:10]] for k in range(K)],
                topw=[[float(beta[k, i]) for i in np.argsort(-beta[k])[:10]] for k in range(K)], size=size / size.sum(),
                main=[c1.BOOKS[b] for b in main], main_share=[float(share[k].max()) for k in range(K)],
                ex_title=c1.BOOKS[int(sbook[ex])], ex_theta=theta[ex], ex_words=words, ex_topic=col,
                book_titles=[c1.BOOKS[b] for b in books], share=share)


# ---------------------------------------------------------------------------
def compute_forward():
    """The forward algorithm and Viterbi on the trained two-state model, checked against every path."""
    import itertools

    h = load("hmm")
    A, B = np.asarray(h["A"]), np.asarray(h["B"])
    pi = np.full(2, 0.5)
    alpha_ = ai1().ALPHA27
    sent = h["sentence"]
    obs = np.array([alpha_.index(ch) for ch in sent])
    T = 6
    o = obs[:T]
    al = np.zeros((T, 2))
    al[0] = pi * B[:, o[0]]
    for t in range(1, T):
        al[t] = (al[t - 1] @ A) * B[:, o[t]]
    brute = 0.0
    for path in itertools.product((0, 1), repeat=T):
        p = pi[path[0]] * B[path[0], o[0]]
        for t in range(1, T):
            p *= A[path[t - 1], path[t]] * B[path[t], o[t]]
        brute += p
    assert abs(al[-1].sum() - brute) < 1e-12 * max(brute, 1e-300) * 1e3
    de = np.zeros((T, 2))
    back = np.zeros((T, 2), int)
    de[0] = pi * B[:, o[0]]
    for t in range(1, T):
        m = de[t - 1][:, None] * A
        back[t] = np.argmax(m, 0)
        de[t] = m.max(0) * B[:, o[t]]
    vp = [int(np.argmax(de[-1]))]
    for t in range(T - 1, 0, -1):
        vp.append(int(back[t][vp[-1]]))
    vp = vp[::-1]
    # the whole sentence, scaled
    a = pi * B[:, obs[0]]
    lp = math.log(a.sum())
    a /= a.sum()
    for t in range(1, len(obs)):
        a = (a @ A) * B[:, obs[t]]
        lp += math.log(a.sum())
        a /= a.sum()
    return dict(letters=sent[:T], alpha=al, brute=brute, delta=de, back=back, vpath=vp, T=T, n=len(obs),
                logp_bits=lp / math.log(2), bits_per_letter=-lp / math.log(2) / len(obs), A=A,
                B_letters=B[:, o])


# ---------------------------------------------------------------------------
# IBM Model 1 (Brown et al., 1993) on a tiny parallel corpus, and BLEU (Papineni et al., 2002)
IBM_TRAIN = [
    ("la maison", "the house"), ("la maison bleue", "the blue house"), ("la fleur", "the flower"),
    ("la fleur bleue", "the blue flower"), ("une maison", "a house"), ("une petite maison", "a small house"),
    ("le chat", "the cat"), ("le chat noir", "the black cat"), ("un chat", "a cat"), ("le chien", "the dog"),
    ("le chien mange", "the dog eats"), ("le chat mange le poisson", "the cat eats the fish"),
    ("le chien voit le chat", "the dog sees the cat"), ("la femme voit la maison", "the woman sees the house"),
    ("une femme mange", "a woman eats"), ("le petit chien", "the small dog"), ("la petite fleur", "the small flower"),
    ("un poisson rouge", "a red fish"), ("la maison rouge", "the red house"),
    ("le chat voit un poisson", "the cat sees a fish"),
]
IBM_TEST = [
    ("le chien noir", "the black dog"), ("la femme mange le poisson", "the woman eats the fish"),
    ("une fleur rouge", "a red flower"), ("le chat voit la femme", "the cat sees the woman"),
    ("un petit chat", "a small cat"), ("la femme voit le chien noir", "the woman sees the black dog"),
]
AFTER_NOUN = {"bleue", "noir", "rouge"}  # French adjectives that follow their noun: the one rule a linguist adds
IBM_EXAMPLE = 11  # le chat mange le poisson


def bleu(hyps, refs, N=4):
    import collections

    num, den = np.zeros(N), np.zeros(N)
    hl = rl = 0
    for h, r in zip(hyps, refs):
        h, r = h.split(), r.split()
        hl, rl = hl + len(h), rl + len(r)
        for n in range(1, N + 1):
            hc = collections.Counter(tuple(h[i:i + n]) for i in range(len(h) - n + 1))
            rc = collections.Counter(tuple(r[i:i + n]) for i in range(len(r) - n + 1))
            num[n - 1] += sum(min(c, rc[g]) for g, c in hc.items())
            den[n - 1] += max(len(h) - n + 1, 0)
    p = num / np.maximum(den, 1)
    bp = 1.0 if hl > rl else math.exp(1 - rl / max(hl, 1))
    score = bp * math.exp(np.mean(np.log(np.maximum(p, 1e-300)))) if (p > 0).all() else 0.0
    return dict(p=p.tolist(), num=num.tolist(), den=den.tolist(), bp=bp, bleu=score, hyp_len=hl, ref_len=rl)


def compute_ibm1():
    pairs = [(f.split(), e.split()) for f, e in IBM_TRAIN]
    F = sorted({w for f, _ in pairs for w in f})
    E = sorted({w for _, e in pairs for w in e})
    fi, ei = {w: i + 1 for i, w in enumerate(F)}, {w: i for i, w in enumerate(E)}  # French 0 is NULL
    t = np.full((len(F) + 1, len(E)), 1.0 / len(E))  # t(e | f): uniform to start
    snaps, aligns, lls = [t.copy()], [], []

    def align(k, t):
        f, e = pairs[k]
        src = [0] + [fi[w] for w in f]
        a = np.array([[t[s, ei[w]] for s in src] for w in e])
        return a / a.sum(1, keepdims=True)

    aligns.append(align(IBM_EXAMPLE, t))
    for it in range(30):
        cnt = np.zeros_like(t)
        ll = 0.0
        for f, e in pairs:
            src = [0] + [fi[w] for w in f]
            for w in e:
                p = t[src, ei[w]]
                ll += math.log(p.sum() / len(src))
                # Repeated source words contribute once per position, even
                # though those positions share a translation-table row.
                np.add.at(cnt[:, ei[w]], src, p / p.sum())
        lls.append(ll)
        t = cnt / np.maximum(cnt.sum(1, keepdims=True), 1e-300)  # M step
        snaps.append(t.copy())
        aligns.append(align(IBM_EXAMPLE, t))
    # Parameter/alignment snapshots contain round zero through round thirty.
    lls.append(sum(math.log(t[[0] + [fi[word] for word in f], ei[w]].sum() / (len(f) + 1))
                   for f, e in pairs for w in e))
    assert all(b >= a - 1e-9 for a, b in zip(lls, lls[1:]))
    best = {f: E[int(np.argmax(t[fi[f]]))] for f in F}

    def gloss(f, reorder):
        out = [best[w] for w in f.split()]
        if reorder:
            for i, w in enumerate(f.split()):
                if w in AFTER_NOUN and i > 0:
                    out[i - 1], out[i] = out[i], out[i - 1]
        return " ".join(out)

    refs = [e for _, e in IBM_TEST]
    h1 = [gloss(f, False) for f, _ in IBM_TEST]
    h2 = [gloss(f, True) for f, _ in IBM_TEST]
    b1, b2 = bleu(h1, refs), bleu(h2, refs)
    show = ["la", "le", "maison", "chat", "chien", "noir", "mange", "voit"]
    return dict(F=F, E=E, t=np.array(snaps), lls=np.array(lls), align=np.array(aligns), example=list(IBM_TRAIN[IBM_EXAMPLE]),
                best=best, test=[list(p) for p in IBM_TEST], hyp_gloss=h1, hyp_rule=h2, bleu_gloss=b1, bleu_rule=b2,
                n_train=len(IBM_TRAIN), show=show,
                show_best=[[best[f], float(t[fi[f]].max())] for f in show])


# ---------------------------------------------------------------------------
def word_ids(text: str):
    import re

    toks = np.array(re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower()))
    return toks


def goodturing_cohort(ia, ib, V):
    """Raw count-of-counts demonstration, not a normalized probability model.

    Missing raw frequency classes make the requested ratio/held mean undefined;
    reject that cohort explicitly rather than fabricate values or emit NaNs.
    """
    ia, ib = np.asarray(ia), np.asarray(ib)
    if (not isinstance(V, (int, np.integer)) or isinstance(V, (bool, np.bool_)) or not 2 <= V <= 3_037_000_499
            or any(x.ndim != 1 or x.dtype.kind not in "iu" or len(x) < 2
                   or np.any(x < 0) or np.any(x >= V) for x in (ia, ib))):
        raise ValueError("Good-Turing requires two nonempty bigram-trial cohorts and a valid vocabulary")
    ia, ib = ia.astype(np.int64, copy=False), ib.astype(np.int64, copy=False)
    trials_a, trials_b = len(ia) - 1, len(ib) - 1
    ka, ca = np.unique(ia[:-1] * V + ia[1:], return_counts=True)
    kb, cb = np.unique(ib[:-1] * V + ib[1:], return_counts=True)
    N0 = float(V) * V - len(ka)
    missing = [r for r in range(1, 9) if not np.any(ca == r)]
    if N0 <= 0 or missing:
        raise ValueError(f"Unsupported raw Good-Turing cohort: unseen types={N0:g}, missing count classes={missing}")
    j = np.minimum(np.searchsorted(kb, ka), len(kb) - 1)
    in_b = np.where(kb[j] == ka, cb[j], 0)
    scale = trials_a / trials_b
    rows = []
    unseen_b = float(cb.sum() - in_b.sum())
    Nr = lambda r: float((ca == r).sum())  # noqa: E731
    rows.append(dict(r=0, Nr=N0, gt=Nr(1) / N0, held=unseen_b * scale / N0))
    for r in range(1, 9):
        sel = ca == r
        rows.append(dict(r=r, Nr=Nr(r), gt=(r + 1) * Nr(r + 1) / Nr(r), held=float(in_b[sel].mean() * scale)))
    disc = [r_["r"] - r_["held"] for r_ in rows[2:]]
    return (dict(rows=rows, discount=disc, types_a=int(len(ka)), bigram_trials_a=trials_a,
                 bigram_trials_b=trials_b, singleton_types=int(Nr(1)), p_unseen=Nr(1) / trials_a), ka, kb)


def continuation_examples(vocab, ia, ib, ka, kb):
    """Actual available frequent-word contrast; a better contrast is not assumed."""
    V = len(vocab)
    # Kneser-Ney's continuation counts on words: frequent, but after very few different words
    allk = np.unique(np.concatenate([ka, kb]))
    prev_n = np.bincount(allk % V, minlength=V)  # N1+(. w): distinct words seen before w
    cnt = np.bincount(np.concatenate([ia, ib]), minlength=V)
    cand = np.nonzero(cnt >= 1000)[0]
    ratio = cnt[cand] / np.maximum(prev_n[cand], 1)
    picks = cand[np.argsort(-ratio)[:6]]
    if not len(picks):
        raise ValueError("Unsupported continuation example cohort: no word occurs at least 1000 times")
    w0 = int(picks[0])
    pre = np.concatenate([ia[:-1][ia[1:] == w0], ib[:-1][ib[1:] == w0]])
    pv, pc = np.unique(pre, return_counts=True)
    if not len(pc):
        raise ValueError("Unsupported continuation example cohort: selected word has no predecessor")
    top_prev = vocab[pv[np.argmax(pc)]]
    # a word about as common, with many different words before it
    near = np.nonzero((cnt > 0.7 * cnt[w0]) & (cnt < 1.4 * cnt[w0]) & (np.arange(V) != w0))[0]
    if not len(near):
        raise ValueError("Unsupported continuation example cohort: no distinct similarly frequent word")
    w1 = int(near[np.argmax(prev_n[near])])
    return dict(example=[[str(vocab[i]), int(cnt[i]), int(prev_n[i])] for i in picks],
                word=str(vocab[w0]), word_count=int(cnt[w0]), word_prev=int(prev_n[w0]), word_top_prev=str(top_prev),
                word_top_share=float(pc.max() / pc.sum()), other=str(vocab[w1]), other_count=int(cnt[w1]),
                other_prev=int(prev_n[w1]))


def compute_goodturing():
    """Raw word-pair count estimates checked on the other half (Church & Gale, 1991)."""
    lines = CACHE.read_text("train").split("\n")
    ta, tb = word_ids("\n".join(lines[0::2])), word_ids("\n".join(lines[1::2]))
    vocab, inv = np.unique(np.concatenate([ta, tb]), return_inverse=True)
    V = len(vocab)
    ia, ib = inv[:len(ta)].astype(np.int64), inv[len(ta):].astype(np.int64)
    cohort, ka, kb = goodturing_cohort(ia, ib, V)
    return dict(cohort, V=V, tokens=int(len(ia) + len(ib)),
                **continuation_examples(vocab, ia, ib, ka, kb))


# ---------------------------------------------------------------------------
# The infinity-gram: a suffix array of the thirty novels
INF_CHUNKS, INF_CHUNK, INF_CAP = 6, 5000, 500
INF_EDGES = (0, 8, 10, 12, 15, 20, 30, 10 ** 9)


def chars_codec():
    train, valid, passage = CACHE.read_text("train"), CACHE.read_text("valid"), CACHE.read_text("passage")
    chars = sorted(set(train) | set(valid) | set(passage))
    idx = {ch: i for i, ch in enumerate(chars)}
    enc = lambda t: np.array([idx[ch] for ch in t], np.int64)  # noqa: E731
    return chars, enc, train, valid, passage


def compute_infini():
    import time

    from videos.ai.ai7.infini import Index

    chars, enc, train, valid, passage = chars_codec()
    K = len(chars)
    if K > 255 or len(train) >= 2 ** 31:
        raise ValueError("The suffix index needs at most255 symbols and signed32-bit positions")
    a, v, ps = enc(train), enc(valid), enc(passage)
    M = int(load("kn")["best"])
    t0 = time.time()
    tables = ngram_tables(a, K, M)
    types = [int(len(t["types"])) for t in tables]  # distinct strings of 1 .. M+1 characters in the novels
    model = kn_model(tables, K, M)
    del tables
    discounts = [float(m["D"]) for m in model]
    print(f"    Kneser-Ney tables in {time.time() - t0:.0f}s", flush=True)
    t0 = time.time()
    idx = Index((a[::-1] + 1).astype(np.uint8))  # the reversed reading: contexts grow leftward
    print(f"    suffix array of {len(a):,} characters in {time.time() - t0:.0f}s", flush=True)

    def infer(seq, positions):
        sc = (seq + 1).astype(np.uint8)
        L = np.zeros(len(positions), np.int32)
        p = np.zeros(len(positions))
        top = np.zeros(len(positions), bool)
        nctx = np.zeros(len(positions), np.int64)
        ntyp = np.zeros(len(positions), np.int64)
        for j, i in enumerate(positions):
            Lj, lo, hi = idx.longest(sc, int(i), cap=INF_CAP)
            if Lj == 0:
                continue
            c = idx.before(lo, hi, K)[1:]
            if c.sum() == 0:
                continue
            L[j], nctx[j], ntyp[j] = Lj, int(c.sum()), int((c > 0).sum())
            p[j] = c[seq[i]] / c.sum()
            top[j] = int(np.argmax(c)) == seq[i]
        return L, p, top, nctx, ntyp

    t0 = time.time()
    g = rng(2024)  # Liu et al., 2024
    starts = np.sort(g.choice(len(v) - INF_CHUNK, size=INF_CHUNKS, replace=False))
    vL, vp, vk, vs = [], [], [], []
    for s in starts:
        ch = v[s:s + INF_CHUNK]
        Lc, pc, _, _, tc = infer(ch, np.arange(M, len(ch)))
        vL.append(Lc)
        vp.append(pc)
        vs.append(tc == 1)
        vk.append(kn_probs(model, ch, K, M))
    vL, vp, vk, vs = np.concatenate(vL), np.concatenate(vp), np.concatenate(vk), np.concatenate(vs)
    pos = np.arange(M, len(ps))
    pL, pp, ptop, pn, pt = infer(ps, pos)
    pk = kn_probs(model, ps, K, M)
    print(f"    longest matches in {time.time() - t0:.0f}s", flush=True)
    # one weight per band of match lengths, chosen on held-out text from the novels (never on the passage)
    # one weight per band of match lengths, and per kind of match: one next character seen (sparse) or several,
    # chosen on held-out text from the novels (never on the passage)
    lams = np.linspace(0, 0.995, 200)
    lam = np.zeros((len(INF_EDGES) - 1, 2))
    for b, (lo, hi) in enumerate(zip(INF_EDGES, INF_EDGES[1:])):
        for sp in (0, 1):
            sel = (vL >= lo) & (vL < hi) & (vs == bool(sp))
            if sel.sum() < 50:
                continue
            ll = [np.log(l_ * vp[sel] + (1 - l_) * vk[sel]).sum() for l_ in lams]
            lam[b, sp] = float(lams[int(np.argmax(ll))])
    band_of = lambda L: np.searchsorted(INF_EDGES, L, side="right") - 1  # noqa: E731
    lam_p = lam[band_of(pL), (pt == 1).astype(int)]
    mix = lam_p * pp + (1 - lam_p) * pk
    mix_bits = float(-np.log2(mix).mean())
    kn_bits_ = float(-np.log2(pk).mean())
    assert abs(kn_bits_ - load("kn")["best_bits"]) < 1e-9  # the same Kneser-Ney, scored the same way
    hist = np.bincount(np.minimum(pL, 40), minlength=41)
    # the counts as one context grows, for the longest match in the passage's first paragraphs
    j = int(np.argmax(pL[:4000]))
    lengths = []
    idx.longest((ps + 1).astype(np.uint8), int(pos[j]), cap=INF_CAP, lengths=lengths)
    i = int(pos[j])
    # a small suffix array, in full, for the picture
    demo = "a rose is a rose"
    dsa = sorted(range(len(demo)), key=lambda k: demo[k:])
    return dict(K=K, n=len(a), M=M, types=types, discounts=discounts, edges=list(INF_EDGES[:-1]), lam=lam, mix_bits=mix_bits,
                kn_bits=kn_bits_, L=pL, hist=hist, mean_L=float(pL.mean()), median_L=float(np.median(pL)),
                max_L=int(pL.max()), acc=float(ptop.mean()), zero=float((pp == 0).mean()),
                sparse=float((pn == 1).mean()), long_count=int((pL >= 10).sum()),
                acc_long=float(ptop[pL >= 10].mean()) if (pL >= 10).any() else None,
                share_long=float((pL >= 10).mean()), grow_context=passage[i - len(lengths):i],
                grow_next=passage[i], grow_counts=lengths, demo=demo, demo_sa=dsa,
                valid_positions=int(len(vL)), example_start=0, example=passage[:160], example_L=pL[:160 - M],
                gain=kn_bits_ - mix_bits)


def compute_scoreboard():
    """The scoreboard as Part 1 left it, with Part 7's two counting rows after Part 1's best counting model."""
    sb = CACHE.read_part1("scoreboard")
    rows = [dict(r) for r in sb["rows"]]
    i = next(j for j, r in enumerate(rows) if r["key"] == "best") + 1
    kn, inf = load("kn"), load("infini")
    rows.insert(i, dict(key="kn", label=rf"Kneser--Ney, \ ${kn['best']}$ characters", bits=kn["best_bits"], part=7,
                        kind="count"))
    rows.insert(i + 1, dict(key="infini", label=r"$\infty$-gram $+$ Kneser--Ney", bits=inf["mix_bits"], part=7,
                            kind="count"))
    return dict(rows=rows, new=[i, i + 1], passage=sb["passage"])


# ---------------------------------------------------------------------------
# Graphical models: d-separation by simulation, belief propagation on a tree
TREE = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]


def compute_dsep():
    g = rng(1988)  # Pearl, 1988
    N = 400_000
    rain = g.random(N) < 0.2
    sprk = g.random(N) < 0.3
    wet = ((rain | sprk) & (g.random(N) < 0.95)) | (g.random(N) < 0.02)
    P = lambda a, b=None: float(a.mean() if b is None else a[b].mean())  # noqa: E731
    # a chain: cloudy -> rain -> wet; a fork: rain <- cloudy -> sprinkler (the sprinkler is used less when it's cloudy)
    cloudy = g.random(N) < 0.5
    rain2 = g.random(N) < np.where(cloudy, 0.6, 0.1)
    sprk2 = g.random(N) < np.where(cloudy, 0.1, 0.5)
    return dict(N=N, collider=dict(p_r=P(rain), p_r_s=P(rain, sprk), p_r_w=P(rain, wet), p_r_ws=P(rain, wet & sprk),
                                   p_r_wns=P(rain, wet & ~sprk)),
                fork=dict(p_s_r=P(sprk2, rain2), p_s_nr=P(sprk2, ~rain2), p_s_rc=P(sprk2, rain2 & cloudy),
                          p_s_nrc=P(sprk2, ~rain2 & cloudy)))


def compute_bp():
    import itertools

    g = rng(1982)  # Pearl's message passing, 1982
    n = 7
    unary = np.exp(g.normal(0, 0.8, (n, 2)))
    pair = {e: np.exp(g.normal(0, 1.0, (2, 2))) for e in TREE}

    def brute(edges):
        Z, marg = 0.0, np.zeros((n, 2))
        for x in itertools.product((0, 1), repeat=n):
            p = np.prod([unary[i, x[i]] for i in range(n)]) * np.prod([pair[e][x[e[0]], x[e[1]]] for e in edges])
            Z += p
            for i in range(n):
                marg[i, x[i]] += p
        return marg / Z

    exact = brute(TREE)
    nb = {i: [] for i in range(n)}
    for a, b in TREE:
        nb[a].append(b)
        nb[b].append(a)

    def psi(i, j):
        return pair[(i, j)] if (i, j) in pair else pair[(j, i)].T

    # two sweeps: leaves to root, root to leaves
    up = [(3, 1), (4, 1), (5, 2), (6, 2), (1, 0), (2, 0)]
    order = up + [(j, i) for i, j in reversed(up)]
    msg = {}
    for i, j in order:
        prod = unary[i].copy()
        for k in nb[i]:
            if k != j:
                prod *= msg[(k, i)]
        m = prod @ psi(i, j)
        msg[(i, j)] = m / m.sum()
    belief = np.array([unary[i] * np.prod([msg[(k, i)] for k in nb[i]], 0) for i in range(n)])
    belief /= belief.sum(1, keepdims=True)
    assert np.allclose(belief, exact, atol=1e-12)
    # one more factor makes a loop (3 - 4): the same messages, repeated, are only approximate
    pair[(3, 4)] = np.exp(g.normal(0, 1.0, (2, 2)))
    loop_edges = TREE + [(3, 4)]
    exact_l = brute(loop_edges)
    nb[3].append(4)
    nb[4].append(3)
    dirs = [(a, b) for a, b in loop_edges] + [(b, a) for a, b in loop_edges]
    lm = {d: np.full(2, 0.5) for d in dirs}
    err = []
    for _ in range(30):
        new = {}
        for i, j in dirs:
            prod = unary[i].copy()
            for k in nb[i]:
                if k != j:
                    prod *= lm[(k, i)]
            m = prod @ psi(i, j)
            new[(i, j)] = m / m.sum()
        lm = new
        bl = np.array([unary[i] * np.prod([lm[(k, i)] for k in nb[i]], 0) for i in range(n)])
        bl /= bl.sum(1, keepdims=True)
        err.append(float(np.abs(bl - exact_l)[:, 1].max()))
    return dict(n=n, edges=TREE, exact=exact[:, 1], belief=belief[:, 1], order=order,
                msgs=[[float(msg[d][1])] for d in order], loopy_err=err, loopy_final=err[-1], states=2 ** n,
                bp_ops=len(order) * 4)


def compute_causal():
    # the kidney-stone study: Charig et al. (1986), as tabulated by Julious & Mullee (1994)
    ks = {"A": {"small": [81, 87], "large": [192, 263]}, "B": {"small": [234, 270], "large": [55, 80]}}
    tot = {t: [sum(v[0] for v in ks[t].values()), sum(v[1] for v in ks[t].values())] for t in ks}
    pz = {z: (ks["A"][z][1] + ks["B"][z][1]) / 700 for z in ("small", "large")}
    adj = {t: sum(ks[t][z][0] / ks[t][z][1] * pz[z] for z in pz) for t in ks}
    # a simulation where we know the truth: severity sways both who is treated and who recovers
    g = rng(2000)  # Pearl, Causality, 2000
    N = 400_000

    def world(do=None):
        z = g.random(N) < 0.5  # severe
        x = (g.random(N) < np.where(z, 0.8, 0.2)) if do is None else (g.random(N) < 0.5)
        y = g.random(N) < 0.5 + 0.1 * x - 0.35 * z
        return z, x, y

    z, x, y = world()
    naive = float(y[x].mean() - y[~x].mean())
    adjusted = float(sum((y[x & (z == s)].mean() - y[~x & (z == s)].mean()) * (z == s).mean() for s in (True, False)))
    strata = [[float(y[x & (z == s)].mean()), float(y[~x & (z == s)].mean())] for s in (False, True)]
    z2, x2, y2 = world(do=True)
    exp_ = float(y2[x2].mean() - y2[~x2].mean())
    return dict(stones=ks, total=tot, pz=pz, adjusted=adj, naive=naive, adjusted_sim=adjusted, experiment=exp_,
                truth=0.1, strata=strata, treated_severe=float(z[x].mean()), untreated_severe=float(z[~x].mean()),
                p_y_x=float(y[x].mean()), p_y_nx=float(y[~x].mean()), N=N)


# ---------------------------------------------------------------------------
# Gaussian processes: the band shrinking as pages land; Occam's razor; Bayesian optimization
def rbf(a, b, ell, s2):
    return s2 * np.exp(-0.5 * (np.asarray(a)[:, None] - np.asarray(b)[None]) ** 2 / ell ** 2)


def gp_post(x, y, xs, ell, s2, n2):
    if len(x) == 0:
        return np.zeros(len(xs)), np.full(len(xs), math.sqrt(s2))
    K = rbf(x, x, ell, s2) + n2 * np.eye(len(x))
    Ks = rbf(xs, x, ell, s2)
    mean = Ks @ np.linalg.solve(K, y)
    var = s2 - np.einsum("ij,ji->i", Ks, np.linalg.solve(K, Ks.T))
    return mean, np.sqrt(np.maximum(var, 0))


GP_NS = (0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 186)


def compute_gpland():
    gp = load("gp")
    x, y, xs = np.asarray(gp["x"]), np.asarray(gp["y"]), np.asarray(gp["xs"])
    ell, s2, n2, mu0 = float(gp["ell"]), float(gp["s2"]), float(gp["noise"]), float(gp["mu0"])
    order = rng(1951).permutation(len(x))  # Krige, 1951
    ns = [min(requested, len(x)) for requested in GP_NS]
    means, sds = [], []
    for n_ in ns:
        sel = order[:n_]
        m, s = gp_post(x[sel], y[sel] - mu0, xs, ell, s2, n2)
        means.append(m + mu0)
        sds.append(s)
    sds = np.array(sds)
    assert all(b <= a + 1e-9 for a, b in zip(sds.mean(1), sds.mean(1)[1:]))  # more data, never wider on average
    return dict(order=order, ns=ns, means=np.array(means), sds=sds, mean_sd=sds.mean(1), s=math.sqrt(s2),
                noise_sd=math.sqrt(n2))


def compute_occam():
    gp = load("gp")
    x, y = np.asarray(gp["x"]), np.asarray(gp["y"]) - float(gp["mu0"])
    s2, n2, best = float(gp["s2"]), float(gp["noise"]), float(gp["ell"])
    ells = np.unique(np.concatenate([np.geomspace(0.4, 120, 70), [best]]))
    fit, comp = [], []
    for ell in ells:
        L = np.linalg.cholesky(rbf(x, x, ell, s2) + n2 * np.eye(len(x)))
        al = np.linalg.solve(L.T, np.linalg.solve(L, y))
        fit.append(float(-0.5 * y @ al))
        comp.append(float(-np.log(np.diag(L)).sum()))
    fit, comp = np.array(fit), np.array(comp)
    total = fit + comp - 0.5 * len(x) * math.log(2 * math.pi)
    # MacKay's evidence for polynomials (Bayesian linear regression, alpha and beta by type-II maximum likelihood)
    g = rng(1992)  # MacKay, Bayesian Interpolation, 1992
    Np = 30
    xp = np.sort(g.uniform(-1, 1, Np))
    f = lambda u: 0.4 - 1.1 * u + 0.3 * u ** 2 + 1.6 * u ** 3  # noqa: E731
    yp = f(xp) + g.normal(0, 0.25, Np)
    degs = list(range(0, 13))
    ev, rmse, fits = [], [], []
    xg = np.linspace(-1, 1, 200)
    for dg in degs:
        Phi = np.polynomial.legendre.legvander(xp, dg)
        Pg = np.polynomial.legendre.legvander(xg, dg)
        a_, b_ = 1.0, 10.0
        for _ in range(500):
            Am = a_ * np.eye(dg + 1) + b_ * Phi.T @ Phi
            m = b_ * np.linalg.solve(Am, Phi.T @ yp)
            lam = np.linalg.eigvalsh(b_ * Phi.T @ Phi)
            gam = float((lam / (a_ + lam)).sum())
            a_ = gam / max(float(m @ m), 1e-12)
            b_ = (Np - gam) / float(((yp - Phi @ m) ** 2).sum())
        Am = a_ * np.eye(dg + 1) + b_ * Phi.T @ Phi
        m = b_ * np.linalg.solve(Am, Phi.T @ yp)
        Em = b_ / 2 * float(((yp - Phi @ m) ** 2).sum()) + a_ / 2 * float(m @ m)
        ev.append(float((dg + 1) / 2 * math.log(a_) + Np / 2 * math.log(b_) - Em - 0.5 * np.linalg.slogdet(Am)[1]
                        - Np / 2 * math.log(2 * math.pi)))
        w_ls = np.linalg.lstsq(Phi, yp, rcond=None)[0]
        rmse.append(float(np.sqrt(((yp - Phi @ w_ls) ** 2).mean())))
        fits.append(Pg @ m)
    return dict(ells=ells, fit=fit, comp=comp, total=total, best_ell=float(ells[np.argmax(total)]), gp_ell=best,
                xp=xp, yp=yp, degs=degs, evidence=np.array(ev), rmse=np.array(rmse), best_deg=int(np.argmax(ev)),
                xg=xg, fits=np.array(fits), true_deg=3)


BO_ORDER, BO_VALID, BO_INIT, BO_STEPS = 5, 200_000, 2, 12


def compute_bayesopt():
    """Bayesian optimization of one hyperparameter: Kneser-Ney's discount D (one D for every order, five characters
    of context), scored by bits per character on held-out text from the novels."""
    from scipy.stats import norm

    chars, enc, train, valid, _ = chars_codec()
    K = len(chars)
    a, v = enc(train), enc(valid)[:BO_VALID]
    base = kn_model(ngram_tables(a, K, BO_ORDER), K, BO_ORDER)
    gt_D = [float(m["D"]) for m in base]
    gt_bits = kn_bits(base, v, K, BO_ORDER)

    def f(D):
        for m in base:
            m["D"] = float(D)
        return kn_bits(base, v, K, BO_ORDER)

    part = CACHE.partial("bayesopt", dict(order=BO_ORDER, valid=BO_VALID))
    grid = np.linspace(0.05, 0.95, 31)
    truth = []
    for D in grid:  # the whole curve, for checking (the optimizer never sees it)
        key = f"grid_{D:.4f}"
        if key not in part:
            part[key] = f(D)
        truth.append(part[key])
    cand = np.linspace(0.02, 0.98, 400)
    g = rng(1975)  # Mockus, 1975
    xs = list(g.uniform(0.05, 0.95, BO_INIT))
    ys = []
    for D in xs:
        key = f"x_{D:.6f}"
        if key not in part:
            part[key] = f(D)
        ys.append(part[key])
    steps = []
    for s in range(BO_STEPS + 1):
        X, Y = np.array(xs), np.array(ys)
        mu, sd = Y.mean(), Y.std() + 1e-9
        Yn = (Y - mu) / sd
        best_ml, ell = -1e18, 0.2
        for e in np.geomspace(0.05, 1.0, 25):  # the length scale by marginal likelihood, as in chapter 14
            Kx = rbf(X, X, e, 1.0) + 1e-6 * np.eye(len(X))
            L = np.linalg.cholesky(Kx)
            al = np.linalg.solve(L.T, np.linalg.solve(L, Yn))
            ml = -0.5 * Yn @ al - np.log(np.diag(L)).sum()
            if ml > best_ml:
                best_ml, ell = ml, e
        m, sdv = gp_post(X, Yn, cand, ell, 1.0, 1e-6)
        best = Yn.min()
        z = (best - m) / np.maximum(sdv, 1e-12)
        ei = np.maximum((best - m) * norm.cdf(z) + sdv * norm.pdf(z), 0)
        nxt = float(cand[int(np.argmax(ei))])
        steps.append(dict(x=X.copy(), y=Y.copy(), mean=m * sd + mu, sd=sdv * sd, ei=ei * sd, next=nxt, ell=ell))
        if s == BO_STEPS or min(abs(nxt - x_) for x_ in xs) < 0.005:  # nowhere left worth looking
            break
        key = f"x_{nxt:.6f}"
        if key not in part:
            part[key] = f(nxt)
        xs.append(nxt)
        ys.append(part[key])
    ib = int(np.argmin(ys))
    return dict(order=BO_ORDER, valid_chars=len(v), grid=grid, truth=np.array(truth), cand=cand,
                xs=np.array(xs), ys=np.array(ys), best_D=float(xs[ib]), best_bits=float(ys[ib]),
                grid_best_D=float(grid[int(np.argmin(truth))]), grid_best_bits=float(min(truth)),
                gt_D=gt_D, gt_bits=gt_bits, evals=len(xs), grid_evals=len(grid),
                steps_x=[st["x"].tolist() for st in steps], steps_y=[st["y"].tolist() for st in steps],
                steps_mean=np.array([st["mean"] for st in steps]), steps_sd=np.array([st["sd"] for st in steps]),
                steps_ei=np.array([st["ei"] for st in steps]), steps_next=[st["next"] for st in steps])


# ---------------------------------------------------------------------------
# Variational inference: coordinate ascent on a model with an exact answer; the reparameterization trick
def compute_cavi():
    """Bishop's example (PRML 10.1.3): pages' rate of "the", a Gaussian of unknown mean and precision, with a
    Normal-Gamma prior.  The posterior is known exactly; mean-field CAVI approximates it by q(mu) q(tau), and
    log p(x) = ELBO + KL(q || posterior) is checked at every step, the KL integrated on a grid."""
    from scipy.special import digamma, gammaln

    X, y, book, vocab = pages()
    g = rng(1999)  # Jordan, Ghahramani, Jaakkola & Saul, 1999
    xs_ = X[np.nonzero(y == 0)[0], vocab.index("the")]
    x = xs_[g.choice(len(xs_), size=25, replace=False)]
    N, xb = len(x), float(x.mean())
    mu0, lam0, a0, b0 = 50.0, 0.01, 1.0, 1.0
    lamN = lam0 + N
    muN = (lam0 * mu0 + N * xb) / lamN
    aN = a0 + N / 2
    bN = b0 + 0.5 * (((x - xb) ** 2).sum() + lam0 * N * (xb - mu0) ** 2 / lamN)
    logp = float(gammaln(aN) - gammaln(a0) + a0 * math.log(b0) - aN * math.log(bN) + 0.5 * math.log(lam0 / lamN)
                 - N / 2 * math.log(2 * math.pi))
    # exact posterior on a grid (mu, tau)
    Etau_post = aN / bN
    sd_mu = 1 / math.sqrt(lamN * Etau_post)
    mug = np.linspace(muN - 7 * sd_mu, muN + 7 * sd_mu, 500)
    from scipy.stats import gamma as G

    taug = np.linspace(G.ppf(1e-7, aN, scale=1 / bN), G.ppf(1 - 1e-7, aN, scale=1 / bN), 500)
    MU, TAU = np.meshgrid(mug, taug)
    logpost = (G.logpdf(TAU, aN, scale=1 / bN) + 0.5 * np.log(lamN * TAU / (2 * math.pi))
               - 0.5 * lamN * TAU * (MU - muN) ** 2)
    dA = (mug[1] - mug[0]) * (taug[1] - taug[0])
    Etau = 1.0 / float(np.var(x)) * 50  # a poor start: fifty times too precise
    hist = []
    for it in range(12):
        m = muN  # q(mu): its mean never changes; its precision follows E[tau]
        lq_ = lamN * Etau
        a = a0 + (N + 1) / 2
        Esq = ((x - m) ** 2).sum() + N / lq_ + lam0 * ((m - mu0) ** 2 + 1 / lq_)
        b = b0 + 0.5 * Esq
        Eltau = digamma(a) - math.log(b)
        Et = a / b
        elbo = (N / 2 * (Eltau - math.log(2 * math.pi)) - Et / 2 * (((x - m) ** 2).sum() + N / lq_)
                + 0.5 * (math.log(lam0) + Eltau - math.log(2 * math.pi)) - lam0 * Et / 2 * ((m - mu0) ** 2 + 1 / lq_)
                + a0 * math.log(b0) - gammaln(a0) + (a0 - 1) * Eltau - b0 * Et
                + 0.5 * (1 + math.log(2 * math.pi) - math.log(lq_))
                + gammaln(a) - (a - 1) * digamma(a) - math.log(b) + a)
        logq = (-0.5 * np.log(2 * math.pi / lq_) - 0.5 * lq_ * (MU - m) ** 2) + G.logpdf(TAU, a, scale=1 / b)
        q = np.exp(logq)
        kl = float((q * (logq - logpost)).sum() * dA)
        mass = float(q.sum() * dA)
        hist.append(dict(m=m, lam=lq_, a=a, b=b, elbo=float(elbo), kl=kl, mass=mass))
        Etau = Et
    gaps = [abs(logp - (h["elbo"] + h["kl"])) for h in hist]
    assert max(gaps) < 1e-3, gaps  # the identity, checked: log p(x) = ELBO + KL
    el = [h["elbo"] for h in hist]
    assert all(b_ >= a_ - 1e-9 for a_, b_ in zip(el, el[1:]))
    # the true posterior's spread of mu, against q's: mean-field is too sure
    sd_true = math.sqrt(bN / (aN - 1) / lamN)  # Student-t marginal
    return dict(x=x, N=N, xbar=xb, prior=[mu0, lam0, a0, b0], post=[muN, lamN, aN, bN], logp=logp,
                elbo=el, kl=[h["kl"] for h in hist], gap=max(gaps), q=[[h["m"], h["lam"], h["a"], h["b"]] for h in hist],
                sd_mu_true=sd_true, sd_mu_q=1 / math.sqrt(hist[-1]["lam"]), iters=len(hist),
                mu_range=[float(mug[0]), float(mug[-1])], tau_range=[float(taug[0]), float(taug[-1])])


def compute_reparam():
    """Two estimates of d/dm E_{z ~ N(m, 1)}[(z - 2)^2] from one sample each: the score function (REINFORCE) and the
    reparameterization z = m + eps.  Both are unbiased; their spreads differ."""
    g = rng(2013)  # Kingma & Welling, 2013
    m, s, R = 0.5, 1.0, 20000
    eps = g.normal(size=R)
    z = m + s * eps
    fz = (z - 2) ** 2
    score = fz * (z - m) / s ** 2
    rep = 2 * (z - 2)
    true = 2 * (m - 2)
    bins = np.linspace(-25, 15, 81)
    return dict(m=m, true=true, score_mean=float(score.mean()), rep_mean=float(rep.mean()), score_sd=float(score.std()),
                rep_sd=float(rep.std()), ratio=float(score.var() / rep.var()), R=R, bins=bins,
                h_score=np.histogram(np.clip(score, -25, 15), bins)[0], h_rep=np.histogram(np.clip(rep, -25, 15), bins)[0])


ITEMS = {
    "pca": compute_pca,
    "gmm": compute_gmm,
    "hmm": compute_hmm,
    "gp": compute_gp,
    "vi": compute_vi,
    "kn": compute_kn,
    "pca2": compute_pca2,
    "ica": compute_ica,
    "embound": compute_embound,
    "kmeans": compute_kmeans,
    "lda": compute_lda,
    "forward": compute_forward,
    "ibm1": compute_ibm1,
    "goodturing": compute_goodturing,
    "infini": compute_infini,
    "scoreboard": compute_scoreboard,
    "dsep": compute_dsep,
    "bp": compute_bp,
    "causal": compute_causal,
    "gpland": compute_gpland,
    "occam": compute_occam,
    "bayesopt": compute_bayesopt,
    "cavi": compute_cavi,
    "reparam": compute_reparam,
}
CACHE.bind(ITEMS)


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
