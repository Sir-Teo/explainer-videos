"""Precompute every number in Part 4 of *Statistics, Built* ("Matrices for Statistics").

    python -m videos.stats.stats4.compute            # everything missing (seconds)
    python -m videos.stats.stats4.compute --force svd

Results are cached in ``.cache/stats4/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Every identity shown on
screen is checked numerically here (an ``assert`` or a reported error), and every distributional claim against a
seeded simulation.  Data from the World: the families (mid-parent and child heights) and the towns.

Items:
    hat        40 families: child height on mid-parent; the hat matrix's eigenvalues and trace; 2,000 simulated
               regressions: E[RSS] = (n - p) sigma^2
    vectors    three heights as a vector in R^3; the mean as the projection onto 1; the residual
    projection Gram-Schmidt on three vectors, QR, and P = A (A'A)^-1 A'
    trace      E[x'Ax] = tr(A Sigma) + mu'A mu, by Monte Carlo
    spectral   the families' 2 x 2 covariance: eigenvalues, eigenvectors, the Rayleigh quotient around the circle
    psd        Cholesky: correlated normals from independent ones
    svd        the World's population map (60 x 100) and its rank-k approximations; Eckart-Young errors
    pinv       an underdetermined system: all solutions, and the minimum-norm one
    blocks     the Schur complement, a block inverse, and a Sherman-Morrison update, checked
    kron       vec(ABC) = (C' kron A) vec(B), checked; a Kronecker covariance's block pattern
    mle        the Gaussian MLE of mean and covariance for 400 families
    quad       z'Hz and z'(I - H)z for z ~ N(0, I_10), p = 3: chi-square 3 and 7
    numerics   near-collinear columns: condition numbers, normal equations vs QR
"""

from __future__ import annotations

import numpy as np
from scipy import linalg, stats

from explainer.ai.cache import Cache
from explainer.stats.world import World

CACHE = Cache("stats4")
load = CACHE.load
W = World()


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def midparent_child(n, seed):
    f = W.families
    g = rng(seed)
    idx = g.choice(len(f["z_child"]), n, replace=False)
    mid = (f["father"][idx] + f["mother"][idx]) / 2
    return mid, f["child"][idx]


# ---------------------------------------------------------------------------
def compute_hat():
    n, p = 40, 2
    x, y = midparent_child(n, 404)
    X = np.column_stack([np.ones(n), x])
    H = X @ np.linalg.solve(X.T @ X, X.T)
    ev = np.sort(np.linalg.eigvalsh(H))[::-1]
    assert np.allclose(H @ H, H, atol=1e-10) and np.isclose(np.trace(H), p)
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    res = y - X @ beta
    # simulation: same X, y = X b + e, e ~ N(0, s^2): E RSS = (n - p) s^2
    g = rng(40)
    s = 5.0
    rss = []
    for _ in range(2000):
        yy = X @ beta + g.normal(0, s, n)
        r = yy - H @ yy
        rss.append(float(r @ r) / s ** 2)
    rss = np.array(rss)
    return {"n": n, "p": p, "x": x, "y": y, "beta": beta, "res": res, "eig": ev, "trace": float(np.trace(H)),
            "rss_mean": float(rss.mean()), "rss": rss, "rss_naive": float((rss / n).mean()),
            "rss_unbiased": float((rss / (n - p)).mean())}


def compute_vectors():
    y = np.array([171.0, 164.0, 181.0])
    one = np.ones(3)
    ybar = y.mean()
    proj = ybar * one
    res = y - proj
    assert abs(res @ one) < 1e-12
    return {"y": y, "mean": float(ybar), "proj": proj, "res": res, "res2": float(res @ res),
            "y2": float(y @ y), "proj2": float(proj @ proj)}


def compute_projection():
    A = np.array([[1.0, 1.0], [1.0, 2.0], [1.0, 4.0]])
    P = A @ np.linalg.solve(A.T @ A, A.T)
    q1 = A[:, 0] / np.linalg.norm(A[:, 0])
    v = A[:, 1] - (A[:, 1] @ q1) * q1
    q2 = v / np.linalg.norm(v)
    Q, R = np.linalg.qr(A)
    assert np.allclose(np.abs(Q[:, 0]), np.abs(q1)) and np.allclose(np.abs(Q[:, 1]), np.abs(q2))
    assert np.allclose(P, np.column_stack([q1, q2]) @ np.column_stack([q1, q2]).T)
    y = np.array([2.0, 1.0, 5.0])
    return {"A": A, "P": P, "q1": q1, "q2": q2, "R": R, "y": y, "Py": P @ y, "res": y - P @ y,
            "eig": np.sort(np.linalg.eigvalsh(P))[::-1], "rank": int(np.linalg.matrix_rank(P)),
            "trace": float(np.trace(P))}


def compute_trace():
    g = rng(2)
    n = 3
    mu = np.array([1.0, -0.5, 2.0])
    L = np.array([[1.0, 0, 0], [0.6, 0.8, 0], [-0.3, 0.4, 0.9]])
    Sigma = L @ L.T
    A = np.array([[2.0, 0.5, 0], [0.5, 1.0, -0.3], [0, -0.3, 1.5]])
    x = mu + g.normal(size=(200_000, n)) @ L.T
    mc = float(np.einsum("ij,jk,ik->i", x, A, x).mean())
    exact = float(np.trace(A @ Sigma) + mu @ A @ mu)
    B = g.normal(size=(3, 5))
    C = g.normal(size=(5, 3))
    return {"mc": mc, "exact": exact, "trAS": float(np.trace(A @ Sigma)), "muAmu": float(mu @ A @ mu),
            "trBC": float(np.trace(B @ C)), "trCB": float(np.trace(C @ B))}


def compute_spectral():
    x, y = midparent_child(400, 7)
    D = np.column_stack([x, y])
    S = np.cov(D.T)
    ev, V = np.linalg.eigh(S)
    order = np.argsort(ev)[::-1]
    ev, V = ev[order], V[:, order]
    th = np.linspace(0, np.pi, 181)
    U = np.column_stack([np.cos(th), np.sin(th)])
    rq = np.einsum("ij,jk,ik->i", U, S, U)
    return {"x": x, "y": y, "S": S, "eig": ev, "V": V, "mean": D.mean(axis=0), "theta": th, "rq": rq,
            "rq_max": float(rq.max()), "rq_min": float(rq.min()), "th_max": float(th[np.argmax(rq)])}


def compute_psd():
    g = rng(1910)
    Sigma = np.array([[1.0, 0.8], [0.8, 1.0]])
    L = np.linalg.cholesky(Sigma)
    z = g.normal(size=(2000, 2))
    x = z @ L.T
    return {"Sigma": Sigma, "L": L, "z": z[:800], "x": x[:800], "cov": np.cov(x.T), "corr": float(np.corrcoef(x.T)[0, 1])}


def compute_svd():
    # the World's population as a 60 x 100 image of the island
    towns = W.towns
    xy, w = towns["xy"], towns["weight"]
    gx, gy = np.meshgrid(np.linspace(-5.2, 5.2, 100), np.linspace(-3.6, 3.6, 60))
    img = np.zeros_like(gx)
    for (tx, ty), ww in zip(xy, w):
        img += ww * np.exp(-((gx - tx) ** 2 + (gy - ty) ** 2) / (2 * 0.18 ** 2))
    img = np.log1p(img / img.max() * 50)
    img = img / img.max()
    U, s, Vt = np.linalg.svd(img, full_matrices=False)
    ks = [1, 2, 5, 10, 25]
    approx = {str(k): (U[:, :k] * s[:k]) @ Vt[:k] for k in ks}
    err = {str(k): float(np.linalg.norm(img - approx[str(k)])) for k in ks}
    ey = {str(k): float(np.sqrt((s[k:] ** 2).sum())) for k in ks}
    for k in ks:
        assert np.isclose(err[str(k)], ey[str(k)])
    energy = np.cumsum(s ** 2) / (s ** 2).sum()
    return {"img": img, "s": s, "ks": ks, **{f"approx_{k}": approx[str(k)] for k in ks}, "err": err, "ey": ey,
            "energy": energy, "storage": {str(k): k * (60 + 100 + 1) for k in ks}, "full": 6000}


def compute_pinv():
    A = np.array([[1.0, 2.0]])
    b = np.array([4.0])
    xmin = np.linalg.pinv(A) @ b
    assert np.allclose(A @ xmin, b)
    return {"A": A, "b": b, "xmin": xmin, "norm": float(np.linalg.norm(xmin))}


def compute_blocks():
    g = rng(5)
    n = 6
    M = g.normal(size=(n, n))
    M = M @ M.T + n * np.eye(n)
    A, B, C, D = M[:3, :3], M[:3, 3:], M[3:, :3], M[3:, 3:]
    S = D - C @ np.linalg.solve(A, B)
    inv = np.linalg.inv(M)
    assert np.allclose(inv[3:, 3:], np.linalg.inv(S))
    assert np.isclose(np.linalg.det(M), np.linalg.det(A) * np.linalg.det(S))
    # Sherman-Morrison: (A + uv')^-1 = A^-1 - A^-1 u v' A^-1 / (1 + v'A^-1 u)
    Ai = np.linalg.inv(M)
    u, v = g.normal(size=n), g.normal(size=n)
    sm = Ai - np.outer(Ai @ u, v @ Ai) / (1 + v @ Ai @ u)
    err = float(np.abs(sm - np.linalg.inv(M + np.outer(u, v))).max())
    return {"err_sm": err, "n": n, "det_ok": True}


def compute_kron():
    g = rng(6)
    A, B, C = g.normal(size=(2, 3)), g.normal(size=(3, 4)), g.normal(size=(4, 2))
    vec = lambda X: X.reshape(-1, order="F")  # noqa: E731
    lhs = vec(A @ B @ C)
    rhs = np.kron(C.T, A) @ vec(B)
    T = np.array([[1.0, 0.6, 0.36], [0.6, 1.0, 0.6], [0.36, 0.6, 1.0]])  # AR(1) in time
    Sp = np.array([[1.0, 0.3], [0.3, 1.0]])  # two sites
    K = np.kron(Sp, T)
    return {"err": float(np.abs(lhs - rhs).max()), "K": K, "T": T, "Sp": Sp}


def compute_mle():
    x, y = midparent_child(400, 11)
    D = np.column_stack([x, y])
    mu = D.mean(axis=0)
    S_mle = (D - mu).T @ (D - mu) / len(D)
    S_unb = np.cov(D.T)
    return {"mu": mu, "S_mle": S_mle, "S_unb": S_unb, "n": len(D)}


def compute_quad():
    g = rng(1876)
    n, p = 10, 3
    X = np.column_stack([np.ones(n), g.normal(size=(n, p - 1))])
    H = X @ np.linalg.solve(X.T @ X, X.T)
    z = g.normal(size=(20_000, n))
    q1 = np.einsum("ij,jk,ik->i", z, H, z)
    M = np.eye(n) - H
    q2 = np.einsum("ij,jk,ik->i", z, M, z)
    xs = np.linspace(0.01, 25, 300)
    return {"n": n, "p": p, "q1": q1, "q2": q2, "xs": xs, "chi_p": stats.chi2.pdf(xs, p),
            "chi_np": stats.chi2.pdf(xs, n - p), "q1_mean": float(q1.mean()), "q2_mean": float(q2.mean()),
            "corr": float(np.corrcoef(q1, q2)[0, 1])}


def compute_numerics():
    g = rng(1947)
    n = 200
    rows = []
    for eps in (1e-1, 1e-3, 1e-5, 1e-7):
        x1 = g.normal(size=n)
        x2 = x1 + eps * g.normal(size=n)
        X = np.column_stack([np.ones(n), x1, x2])
        beta = np.array([1.0, 2.0, 3.0])
        y = X @ beta
        kX = float(np.linalg.cond(X))
        b_ne = np.linalg.solve(X.T @ X, X.T @ y)
        Q, R = np.linalg.qr(X)
        b_qr = linalg.solve_triangular(R, Q.T @ y)
        rows.append({"eps": eps, "condX": kX, "condXtX": float(np.linalg.cond(X.T @ X)),
                     "err_ne": float(np.abs(b_ne - beta).max()), "err_qr": float(np.abs(b_qr - beta).max())})
    return {"rows": rows, "machine_eps": float(np.finfo(float).eps)}


ITEMS = {
    "hat": compute_hat, "vectors": compute_vectors, "projection": compute_projection, "trace": compute_trace,
    "spectral": compute_spectral, "psd": compute_psd, "svd": compute_svd, "pinv": compute_pinv,
    "blocks": compute_blocks, "kron": compute_kron, "mle": compute_mle, "quad": compute_quad,
    "numerics": compute_numerics,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
