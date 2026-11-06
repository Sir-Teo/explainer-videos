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
    Q, _ = np.linalg.qr(A)
    R = np.column_stack([q1, q2]).T @ A
    assert np.allclose(np.abs(Q[:, 0]), np.abs(q1)) and np.allclose(np.abs(Q[:, 1]), np.abs(q2))
    basis = np.column_stack([q1, q2])
    assert np.allclose(basis @ R, A)
    assert np.allclose(P, basis @ basis.T)
    y = np.array([3.0, -1.0, 3.0])
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
    Ai_block, Si = np.linalg.inv(A), np.linalg.inv(S)
    block_inverse = np.block([[Ai_block + Ai_block @ B @ Si @ C @ Ai_block, -Ai_block @ B @ Si],
                              [-Si @ C @ Ai_block, Si]])
    err_block = float(np.abs(block_inverse - inv).max())
    assert np.allclose(block_inverse, inv)
    # Sherman-Morrison: (A + uv')^-1 = A^-1 - A^-1 u v' A^-1 / (1 + v'A^-1 u)
    Ai = np.linalg.inv(M)
    u, v = g.normal(size=n), g.normal(size=n)
    sm = Ai - np.outer(Ai @ u, v @ Ai) / (1 + v @ Ai @ u)
    err = float(np.abs(sm - np.linalg.inv(M + np.outer(u, v))).max())
    return {"err_sm": err, "err_block": err_block, "n": n, "det_ok": True}


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


def compute_extras():
    """Sections added to chapters 1-12: ANOVA by nested projections, Mahalanobis, the dummy trap, Frisch-Waugh-Lovell,
    noncentral chi-square, centring."""
    out = {}
    # --- ANOVA as nested projections (the hat data)
    x, y = midparent_child(40, 404)
    n = len(y)
    one = np.ones(n)
    X = np.column_stack([one, x])
    P1 = np.outer(one, one) / n
    PX = X @ np.linalg.solve(X.T @ X, X.T)
    ss_tot = float(y @ (np.eye(n) - P1) @ y)
    ss_reg = float(y @ (PX - P1) @ y)
    ss_res = float(y @ (np.eye(n) - PX) @ y)
    assert np.isclose(ss_tot, ss_reg + ss_res)
    out["anova"] = {"tot": ss_tot, "reg": ss_reg, "res": ss_res, "r2": ss_reg / ss_tot,
                    "tr": [1.0, float(np.trace(PX - P1)), float(np.trace(np.eye(n) - PX))]}
    # --- generalized variance
    xs, ys = midparent_child(400, 7)
    S = np.cov(np.column_stack([xs, ys]).T)
    ev = np.linalg.eigvalsh(S)
    out["genvar"] = {"det": float(np.linalg.det(S)), "prod": float(ev.prod()), "tr": float(np.trace(S)), "sum": float(ev.sum())}
    # --- Mahalanobis: who is unusual?
    D = np.column_stack([xs, ys])
    mu = D.mean(axis=0)
    Si = np.linalg.inv(S)
    md = np.sqrt(np.einsum("ij,jk,ik->i", D - mu, Si, D - mu))
    ed = np.linalg.norm((D - mu) / D.std(axis=0), axis=1)
    i_m = int(np.argmax(md))
    # a point unusual in Mahalanobis but ordinary in each coordinate: tall parents, short child, etc.
    score = md - ed
    i_odd = int(np.argmax(score))
    w, V = np.linalg.eigh(S)
    root_inv = V @ np.diag(w ** -0.5) @ V.T
    white = (D - mu) @ root_inv.T
    out["maha"] = {"x": xs, "y": ys, "mu": mu, "S": S, "md": md, "i_max": i_m, "i_odd": i_odd,
                   "white": white, "white_cov": np.cov(white.T), "md_odd": float(md[i_odd]), "ed_odd": float(ed[i_odd]),
                   "chi2_95": float(stats.chi2.ppf(0.95, 2)), "frac_out": float((md ** 2 > stats.chi2.ppf(0.95, 2)).mean())}
    # --- Var(Ax): heights to (mean, difference)
    A = np.array([[0.5, 0.5], [1.0, -1.0]])
    out["lin"] = {"A": A, "ASA": A @ S @ A.T, "emp": np.cov((D @ A.T).T)}
    # --- PCA via SVD of the centred data
    Dc = D - mu
    U, sv, Vt = np.linalg.svd(Dc, full_matrices=False)
    out["pca"] = {"sv2": (sv ** 2 / (len(D) - 1)), "eig": np.sort(ev)[::-1], "Vt": Vt, "share": float(sv[0] ** 2 / (sv ** 2).sum())}
    # --- the dummy-variable trap: 3 regions, intercept + 3 indicators
    g = rng(31)
    reg = np.repeat([0, 1, 2], 4)
    yr = np.array([62.0, 58, 61, 59, 70, 72, 69, 73, 55, 53, 57, 54]) + 0 * g.normal(size=12)
    Xd = np.column_stack([np.ones(12), reg == 0, reg == 1, reg == 2]).astype(float)
    rank = int(np.linalg.matrix_rank(Xd))
    bmin = np.linalg.pinv(Xd) @ yr
    alt = bmin + 5.0 * np.array([1, -1, -1, -1])  # another least-squares solution (null space direction)
    assert np.allclose(Xd @ alt, Xd @ bmin)
    means = [float(yr[reg == k].mean()) for k in range(3)]
    out["dummy"] = {"rank": rank, "bmin": bmin, "alt": alt, "means": means, "y": yr, "reg": reg,
                    "diff_min": float(bmin[2] - bmin[1]), "diff_alt": float(alt[2] - alt[1]), "null": [1, -1, -1, -1]}
    # --- Frisch-Waugh-Lovell: child on father and mother
    f = W.families
    idx = rng(77).choice(len(f["child"]), 300, replace=False)
    fa, mo, ch = f["father"][idx], f["mother"][idx], f["child"][idx]
    Xf = np.column_stack([np.ones(300), fa, mo])
    b_full = np.linalg.lstsq(Xf, ch, rcond=None)[0]
    Z = np.column_stack([np.ones(300), fa])
    Mz = np.eye(300) - Z @ np.linalg.solve(Z.T @ Z, Z.T)
    ry, rx = Mz @ ch, Mz @ mo
    b_fwl = float(rx @ ry / (rx @ rx))
    b_simple = float(np.polyfit(mo, ch, 1)[0])
    assert np.isclose(b_fwl, b_full[2])
    out["fwl"] = {"b_full": b_full, "b_fwl": b_fwl, "b_simple": b_simple, "rx": rx, "ry": ry,
                  "corr_fm": float(np.corrcoef(fa, mo)[0, 1])}
    # --- noncentral chi-square: z + mu
    nn, pp = 10, 3
    Xq = np.column_stack([np.ones(nn), rng(1876).normal(size=(nn, pp - 1))])
    H = Xq @ np.linalg.solve(Xq.T @ Xq, Xq.T)
    M = np.eye(nn) - H
    gq = rng(9)
    deltas = [0.0, 2.0, 4.0]
    ncs = {}
    for dl in deltas:
        mu_v = M @ gq.normal(size=nn)
        mu_v = mu_v / np.linalg.norm(mu_v) * dl
        z = gq.normal(size=(20_000, nn)) + mu_v
        q = np.einsum("ij,jk,ik->i", z, M, z)
        ncs[str(dl)] = {"mean": float(q.mean()), "theory": float(nn - pp + dl ** 2),
                        "power": float((q > stats.chi2.ppf(0.95, nn - pp)).mean()),
                        "power_theory": float(stats.ncx2.sf(stats.chi2.ppf(0.95, nn - pp), nn - pp, dl ** 2)) if dl > 0 else 0.05,
                        "q": q[:20000]}
    out["ncx2"] = ncs
    out["ncx2_xs"] = np.linspace(0.01, 40, 300)
    out["ncx2_pdf"] = {str(dl): (stats.ncx2.pdf(out["ncx2_xs"], nn - pp, dl ** 2) if dl > 0 else stats.chi2.pdf(out["ncx2_xs"], nn - pp))
                       for dl in deltas}
    # --- centring: polynomial regression on heights
    hx = W.height[W.sample(200, among=W.adult, seed=4)]
    Xraw = np.column_stack([np.ones(200), hx, hx ** 2])
    hc = hx - hx.mean()
    Xcen = np.column_stack([np.ones(200), hc, hc ** 2])
    out["centre"] = {"raw": float(np.linalg.cond(Xraw)), "cen": float(np.linalg.cond(Xcen)),
                     "corr_raw": float(np.corrcoef(hx, hx ** 2)[0, 1]), "corr_cen": float(np.corrcoef(hc, hc ** 2)[0, 1])}
    # --- Kronecker eigenvalues
    T = np.array([[1.0, 0.6, 0.36], [0.6, 1.0, 0.6], [0.36, 0.6, 1.0]])
    Sp = np.array([[1.0, 0.3], [0.3, 1.0]])
    e_k = np.sort(np.linalg.eigvalsh(np.kron(Sp, T)))
    e_p = np.sort(np.outer(np.linalg.eigvalsh(Sp), np.linalg.eigvalsh(T)).ravel())
    out["kron_eig"] = {"kron": e_k, "prod": e_p, "err": float(np.abs(e_k - e_p).max())}
    return nest(out)


def compute_extras2():
    out = {}
    # leverage: diag(H) for the hook's 40 families
    x, y = midparent_child(40, 404)
    X = np.column_stack([np.ones(40), x])
    H = X @ np.linalg.solve(X.T @ X, X.T)
    h = np.diag(H)
    out["lev"] = {"x": x, "y": y, "h": h, "sum": float(h.sum()), "i_max": int(np.argmax(h)), "max": float(h.max()),
                  "formula": (1 / 40 + (x - x.mean()) ** 2 / ((x - x.mean()) ** 2).sum()).tolist()}
    # leave-one-out residuals: e_i / (1 - h_ii) vs refitting 40 times
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    loo_formula = e / (1 - h)
    loo_direct = []
    for i in range(40):
        m = np.arange(40) != i
        bi = np.linalg.lstsq(X[m], y[m], rcond=None)[0]
        loo_direct.append(float(y[i] - X[i] @ bi))
    loo_direct = np.array(loo_direct)
    out["loo"] = {"formula": loo_formula, "direct": loo_direct, "err": float(np.abs(loo_formula - loo_direct).max()),
                  "press": float((loo_formula ** 2).sum()), "rss": float((e ** 2).sum())}
    # power iteration on the families' covariance
    xs, ys = midparent_child(400, 7)
    S = np.cov(np.column_stack([xs, ys]).T)
    v = np.array([1.0, 0.0])
    lam_true = float(np.linalg.eigvalsh(S).max())
    its = []
    for k in range(12):
        v = S @ v
        v = v / np.linalg.norm(v)
        its.append({"v": v.tolist(), "lam": float(v @ S @ v)})
    ev = np.sort(np.linalg.eigvalsh(S))
    out["power"] = {"its": its, "lam": lam_true, "ratio": float(ev[0] / ev[1])}
    # independence of mean and variance: normal vs exponential samples of 10
    g = rng(1908)
    zn = g.normal(size=(20_000, 10))
    ze = g.exponential(size=(20_000, 10))
    out["indep"] = {"n_mean": zn.mean(axis=1)[:3000], "n_var": zn.var(axis=1, ddof=1)[:3000],
                    "e_mean": ze.mean(axis=1)[:3000], "e_var": ze.var(axis=1, ddof=1)[:3000],
                    "n_corr": float(np.corrcoef(zn.mean(axis=1), zn.var(axis=1, ddof=1))[0, 1]),
                    "e_corr": float(np.corrcoef(ze.mean(axis=1), ze.var(axis=1, ddof=1))[0, 1])}
    # catastrophic cancellation: heights measured from far away (an offset of 1e8 cm)
    hgt = W.height[W.sample(1000, among=W.adult, seed=12)].astype(np.float64)
    rows = []
    for off in (0.0, 1e4, 1e6, 1e8):
        xx = hgt + off
        n = len(xx)
        naive = (np.sum(xx * xx) - n * np.mean(xx) ** 2) / (n - 1)
        two = np.sum((xx - xx.mean()) ** 2) / (n - 1)
        rows.append({"off": off, "naive": float(naive), "two": float(two)})
    out["cancel"] = {"rows": rows, "true": float(np.var(hgt, ddof=1))}
    return nest(out)


def compute_extras3():
    out = {}
    # nearest correlation matrix by Higham's alternating projections (2002)
    B = np.array([[1, 0.9, -0.9], [0.9, 1, 0.9], [-0.9, 0.9, 1.0]])
    Y = B.copy()
    dS = np.zeros_like(B)
    for _ in range(200):
        R = Y - dS
        w, V = np.linalg.eigh(R)
        X = V @ np.diag(np.clip(w, 0, None)) @ V.T
        dS = X - R
        Y = X.copy()
        np.fill_diagonal(Y, 1.0)
    out["nearcorr"] = {"bad_eig": np.linalg.eigvalsh(B), "fixed": Y, "fixed_eig": np.linalg.eigvalsh(Y),
                       "dist": float(np.linalg.norm(Y - B))}
    # ridge path for the dummy design -> the pseudoinverse solution as lambda -> 0
    reg = np.repeat([0, 1, 2], 4)
    yr = np.array([62.0, 58, 61, 59, 70, 72, 69, 73, 55, 53, 57, 54])
    Xd = np.column_stack([np.ones(12), reg == 0, reg == 1, reg == 2]).astype(float)
    lams = np.logspace(2, -6, 60)
    path = np.array([np.linalg.solve(Xd.T @ Xd + l * np.eye(4), Xd.T @ yr) for l in lams])
    out["ridge"] = {"lams": np.log10(lams), "path": path, "pinv": np.linalg.pinv(Xd) @ yr}
    # a space-time field from the Kronecker covariance: 2 sites x 60 times, AR(1) rho = 0.9, site corr 0.7
    g = rng(39)
    nt = 60
    rho = 0.9
    T = rho ** np.abs(np.subtract.outer(np.arange(nt), np.arange(nt)))
    Sp = np.array([[1.0, 0.7], [0.7, 1.0]])
    L = np.kron(np.linalg.cholesky(Sp), np.linalg.cholesky(T))
    z = L @ g.normal(size=2 * nt)
    out["field"] = {"a": z[:nt], "b": z[nt:], "corr": float(np.corrcoef(z[:nt], z[nt:])[0, 1])}
    return nest(out)


def nest(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    return obj


ITEMS = {
    "hat": compute_hat, "vectors": compute_vectors, "projection": compute_projection, "trace": compute_trace,
    "spectral": compute_spectral, "psd": compute_psd, "svd": compute_svd, "pinv": compute_pinv,
    "blocks": compute_blocks, "kron": compute_kron, "mle": compute_mle, "quad": compute_quad,
    "numerics": compute_numerics, "extras": compute_extras,
    "extras2": compute_extras2, "extras3": compute_extras3,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
