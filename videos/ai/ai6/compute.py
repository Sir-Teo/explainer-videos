"""Precompute everything numerical in Part 6 of the AI series ("Statistical ML").

    python -m videos.ai.ai6.compute              # everything missing (needs Part 1's books and Part 5's pages)
    python -m videos.ai.ai6.compute --force hmm

Results are cached in ``.cache/ai6/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Every method is written
out here in numpy, and every number the narration quotes is computed here.

Items:
    pca      principal components of Part 5's 639 pages (70 word rates each, standardized): the variance each
             direction explains, the pages in the first three, and the words that load on the first two
    gmm      a mixture of two Gaussians fitted by EM to the pages' first two principal components, with no labels:
             every iteration's means, covariances, weights and log-likelihood; agreement with the true authors
    hmm      a two-state hidden Markov model fitted by Baum-Welch to 200,000 letters of the books: the emission
             probabilities at each iteration, the transition matrix, and the most likely states of a sentence
    gp       Gaussian-process regression on the rate of "her" across the pages of Great Expectations: the length
             scale chosen by marginal likelihood, prior and posterior samples, the mean and its band
    vi       variational inference on Part 4's two-bump density: the best single Gaussian under KL(q||p) and under
             KL(p||q), and the path of gradient steps on the ELBO
    kn       Kneser-Ney smoothing for character n-grams on Part 1's books, up to 7 characters of context: bits per character on the
             passage, the scoreboard's new row
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai6")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def ai1():
    from videos.ai.ai1 import compute as c1

    return c1


def pages():
    from videos.ai.ai5 import compute as c5

    p = c5.load("pages")
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
    assert share[0] > share[1] > share[2] and split > 0.8
    return dict(share=share, proj=proj, y=y, top=top, split=split, n=len(y), d=X.shape[1])


# ---------------------------------------------------------------------------
def gauss_logpdf(X, m, S):
    d = X - m
    inv = np.linalg.inv(S)
    return -0.5 * np.einsum("ni,ij,nj->n", d, inv, d) - 0.5 * math.log(np.linalg.det(2 * math.pi * S))


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
        covs = np.array([((r[:, k:k + 1] * (P - means[k])).T @ (P - means[k])) / nk[k] + 1e-6 * np.eye(2)
                         for k in range(2)])
    lls = [h["ll"] for h in hist]
    assert all(b >= a - 1e-9 for a, b in zip(lls, lls[1:]))  # EM never goes downhill
    lab = hist[-1]["r"] > 0.5
    agree = float(max((lab == y).mean(), (lab != y).mean()))
    del g
    return dict(P=P, y=y, means=np.array([h["means"] for h in hist]), covs=np.array([h["covs"] for h in hist]),
                w=np.array([h["w"] for h in hist]), ll=np.array(lls), r=np.array([h["r"] for h in hist]),
                agree=agree)


# ---------------------------------------------------------------------------
HMM_LETTERS = 200_000


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
    t = c1.text("train27")[:HMM_LETTERS]
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
    assert set("aeiou") <= set(vowel_side), vowel_side
    sent = c1.to27("There is no reverse on a motorcycle")
    states = viterbi(np.array([alpha.index(ch) for ch in sent]), A, B, np.full(2, 0.5))  # no memory of the books' start
    assert [s_ == 0 for s_ in states] == [B[0, alpha.index(ch)] > B[1, alpha.index(ch)] for ch in sent]
    assert all(b >= a - 1e-9 for a, b in zip(lls, lls[1:]))
    return dict(A=A, B=B, pi=pi, Bs=Bs, lls=lls / math.log(2), vowel_side=vowel_side, sentence=sent, states=states,
                n=HMM_LETTERS, post=post)


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
    assert best[2] > best[3]  # more signal than noise: the rate really drifts from page to page
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
    from videos.ai.ai4.compute import density2

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
    minimize(kl_qp, th0, method="Nelder-Mead", callback=lambda th: path.append(th.copy()),
             options=dict(maxiter=600, xatol=1e-4, fatol=1e-7))
    t_qp = path[-1]
    assert t_qp[0] < -1.2  # the reverse KL settles on one bump: the bigger one, on the left
    # KL(p||q) is minimized exactly by moment matching: the Gaussian with p's own mean and covariance
    mean_p = p @ G
    cov_p = ((G - mean_p) * p[:, None]).T @ (G - mean_p)
    sd_p = np.sqrt(np.diag(cov_p))
    t_pq = np.array([*mean_p, *np.log(sd_p), math.atanh(cov_p[0, 1] / (sd_p[0] * sd_p[1]))])
    assert kl_pq(t_pq) < kl_pq(t_qp) and kl_qp(t_qp) < kl_qp(t_pq)  # each fit wins under its own measure
    pick = np.linspace(0, len(path) - 1, 40).astype(int)
    return dict(path=np.array(path)[pick], t_qp=t_qp, t_pq=t_pq, mean_p=mean_p, cov_p=cov_p,
                kl_qp=[kl_qp(path[k]) for k in pick], kl_final=kl_qp(t_qp), kl_pq_final=kl_pq(t_pq))


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


def kn_bits(model, a, K, M):
    """Bits per symbol of the sequence a under the model with context length M (the first M symbols are skipped)."""
    return float(-np.log2(kn_probs(model, a, K, M)).mean())


def kn_probs(model, a, K, M):
    """The model's probability of each symbol of a, from position M on."""
    n = len(a)
    idx = np.arange(M, n)
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
    c1 = ai1()
    train, valid, passage = c1.text("train"), c1.text("valid"), c1.text("passage")
    chars = sorted(set(train) | set(valid) | set(passage))
    idx = {ch: i for i, ch in enumerate(chars)}
    K = len(chars)
    enc = lambda t: np.array([idx[ch] for ch in t], np.int64)  # noqa: E731
    a, v, ps = enc(train), enc(valid), enc(passage)
    MAXM = max(m for m in range(1, 10) if K ** (m + 1) < 2 ** 62)  # n-gram keys must fit in 64 bits
    rows = []
    tables = ngram_tables(a, K, MAXM)
    for M in range(0, MAXM + 1):
        model = kn_model(tables, K, M)
        rows.append(dict(order=M, valid=kn_bits(model, v, K, M), test=kn_bits(model, ps, K, M)))
        print(f"    KN order {M}: valid {rows[-1]['valid']:.3f}  passage {rows[-1]['test']:.3f}")
    best = int(np.argmin([r["valid"] for r in rows]))
    raw = c1.load("raw")
    assert rows[best]["test"] < raw["best_bits"]  # better than Part 1's best counting model
    return dict(K=K, rows=rows, best=best, best_bits=rows[best]["test"], part1_best=raw["best_bits"],
                part1_rows=[r["test"] for r in raw["rows"]])


ITEMS = {
    "pca": compute_pca,
    "gmm": compute_gmm,
    "hmm": compute_hmm,
    "gp": compute_gp,
    "vi": compute_vi,
    "kn": compute_kn,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
